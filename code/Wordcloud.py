#!/usr/bin/env python
# coding: utf-8

import os

# Install the required libraries
os.system('pip install konlpy')
os.system('pip install nltk')
os.system('pip install matplotlib')
os.system('pip install wordcloud')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.common.keys import Keys
import math
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pymysql
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
from pyspark.sql import SparkSession

# Get the name as input
name = input("Enter your name: ")

pymysql.install_as_MySQLdb()

user = "root"
password = "Sangjin<1"
database = "db_web_project"
engine = create_engine(f"mysql+mysqldb://{user}:{password}@172.31.21.49:3306/{database}",
                       connect_args={'charset':'utf8mb4'})
conn = engine.connect

connect = pymysql.connect(host='172.31.21.49', user='root', password='Sangjin<1', charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
cur = connect.cursor()

query = f"SELECT * FROM db_web_project.final_review_df WHERE NAME_AND_DONG = '{name}'"
cur.execute(query)
result = cur.fetchall()

df = pd.DataFrame(result)

df1 = pd.DataFrame()
positive = []
negative = []

# Separate reviews into positive and negative based on score
for i, j in zip(df['SCORE'], df['REVIEW']):
    if int(i) < 4:
        negative.append(j)
    else:
        positive.append(j)     

# Word Cloud for Positive Reviews
positive_lst = ''.join(positive)
if positive_lst:
    from konlpy.tag import Okt
    import nltk
    from wordcloud import WordCloud, STOPWORDS

    okt = Okt() 
    a = okt.nouns(positive_lst)
    b = nltk.Text(a)
    b = b.vocab().most_common(50)

    wordcloud = WordCloud(font_path="malgun.ttf", 
                          stopwords=STOPWORDS, 
                          background_color="black", 
                          colormap="Blues", 
                          width=1000, height=800).generate_from_frequencies(dict(b))

    plt.figure(figsize=(5,5))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

# Word Cloud for Negative Reviews
negative_lst = ''.join(negative)
if negative_lst:
    from konlpy.tag import Okt
    import nltk
    from wordcloud import WordCloud, STOPWORDS

    okt = Okt() 
    c = okt.nouns(negative_lst)
    d = nltk.Text(c)
    d = d.vocab().most_common(50)

    wordcloud = WordCloud(font_path="malgun.ttf", 
                          stopwords=STOPWORDS, 
                          background_color="black", 
                          colormap="Blues", 
                          width=1000, height=800).generate_from_frequencies(dict(d))

    plt.figure(figsize=(5,5))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
