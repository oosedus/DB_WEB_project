#!/usr/bin/env python
# coding: utf-8

# Install the required library
get_ipython().system('pip install konlpy')

# Import the necessary libraries
import re
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType, StringType
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import when
from pyspark.ml.feature import HashingTF, Tokenizer, VectorAssembler
from pyspark.ml.classification import LogisticRegression

# Create a Spark session
spark = SparkSession.builder \
    .appName("sentimental_analysis") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .master("yarn").getOrCreate()

# Set HDFS configuration
spark.conf.set("fs.defaultFS", "hdfs://54.252.183.196:8020")
spark.conf.set("spark.hadoop.fs.defaultFS", "hdfs://54.252.183.196:8020")

# Load the data from HDFS
data = spark.read.format("csv").option("header", "false") \
    .option("inferSchema", "false")\
        .load("hdfs://54.252.183.196:8020/home/hadoop/training_review_data/")

# Define a function to remove special characters, emojis, and symbols
def remove_special_chars(text):
    pattern = r'[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9\s\U00010000-\U0010ffff]'
    return re.sub(pattern, '', text)

# Register the function as a PySpark UDF
remove_special_chars_udf = udf(remove_special_chars, StringType())

# Remove special characters, emojis, and symbols from the review text
data = data.withColumn("cleaned_review", remove_special_chars_udf(data["_c3"]))

# Assign labels based on the score (positive if score >= 4, negative if score <= 2.5)
data = data.withColumn("label", when(data["_c2"] >= 4.0, 1).when(data["_c2"] <= 2.5, 0))
data = data.filter((data["_c2"] >= 4) | (data["_c2"] <= 2.5))
data = data.withColumn("label", (data["_c2"] >= 4).cast("integer"))

# Split the data into train and test sets
(trainData, testData) = data.randomSplit([0.8, 0.2], seed=100)

# Tokenize the review text
tokenizer = Tokenizer(inputCol="cleaned_review", outputCol="words")

# Vectorize the words
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")

# Assemble the features into a vector
assembler = VectorAssembler(inputCols=["features"], outputCol="feature_vector")

# Create a logistic regression model
lr = LogisticRegression(labelCol="label", featuresCol="feature_vector")

# Create a pipeline for the entire process
pipeline = Pipeline(stages=[tokenizer, hashingTF, assembler, lr])

# Fit the pipeline to the training data
lr_model = pipeline.fit(trainData)

# Use the trained model to make predictions on the test data
predictions = lr_model.transform(testData)

# Evaluate the accuracy of the predictions
evaluator = BinaryClassificationEvaluator(labelCol="label")
accuracy = evaluator.evaluate(predictions)
print("Accuracy:", accuracy)

# Calculate TP, FP, TN, FN
tp = predictions.filter("label = 1 and prediction = 1").count()
fp = predictions.filter("label = 0 and prediction = 1").count()
tn = predictions.filter("label = 0 and prediction = 0").count()
fn = predictions.filter("label = 1 and prediction = 0").count()

# Calculate precision, recall, and F1 score
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2 * (precision * recall) / (precision + recall)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1_score)

# Calculate the AUC
evaluator = BinaryClassificationEvaluator(labelCol="label", metricName="areaUnderROC")
auc = evaluator.evaluate(predictions)
print("AUC:", auc)

# Load the review data from HDFS
review = spark.read.format("csv").option("header", "false")\
    .option("inferSchema", "false")\
    .load("hdfs://54.252.183.196:8020/home/hadoop/review_df/part-m-00000")

# 컬럼 타입 변환
review = review.withColumn("_c3", review["_c3"].cast(StringType()))

# null 값을 다른 값으로 대체
replacement_values = {"_c0": "N/A", "_c1": "N/A", "_c2": "N/A", "_c3": "N/A"}
review = review.fillna(replacement_values)

# 이모티콘 제거하여 새로운 컬럼 생성
review = review.withColumn("cleaned_review", remove_special_chars_udf(review["_c3"]))

# 학습된 모델을 사용하여 테스트 데이터 예측
pred_score = lr_model.transform(review)

tmp_df = pred_score.select("_c0","_c3","prediction")
tmp_df = tmp_df.withColumn("prediction", col("prediction").cast(StringType()))

output_path = "hdfs://54.252.183.196:8020/home/hadoop/real_review_df/"

from pyspark.sql.functions import monotonically_increasing_id

# 각 행에 고유한 ID 생성
review = review.withColumn("id", monotonically_increasing_id())
tmp_df = tmp_df.withColumn("id", monotonically_increasing_id())

# id를 기준으로 조인
joined_df = review.join(tmp_df, review.id == tmp_df.id, 'inner')

# 필요한 경우 id 컬럼 제거
joined_df = joined_df.drop(review.id)
joined_df = joined_df.drop(tmp_df.id)

# 'prediction' 컬럼을 'label' 컬럼으로 추가
joined_df = joined_df.withColumn("label", joined_df["prediction"])

# 중복되는 컬럼 제거
joined_df = joined_df.drop(tmp_df._c0)
joined_df = joined_df.drop(tmp_df._c3)
joined_df = joined_df.drop(tmp_df.prediction)
joined_df = joined_df.drop("cleaned_review")

joined_df = joined_df.select('_c0', '_c1', '_c2', '_c3', 'label')

# Save the joined DataFrame to HDFS
joined_df.write.format("csv").option("header", "false").mode("append").save(output_path)
