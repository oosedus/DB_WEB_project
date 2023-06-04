from flask import Flask, render_template, request, session, jsonify
import pandas as pd

import mysql.connector
from sqlalchemy import create_engine
import pymysql
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
from matplotlib import style

import os

app = Flask(__name__)
app.secret_key = 'sangjin'  # app.py와 동일한 secret_key 값으로 설정

def sickdang_wc(unique_key):
    # cnx = mysql.connector.connect(
    # host='172.31.21.49',
    # user='root',
    # password='Sangjin<1',
    # database='db_web_project'
    # )
    # cursor = cnx.cursor()
    # cursor.execute('USE db_web_project')
    # print(f"{unique_key}uniquekey in wc.py")

    try:
        pymysql.install_as_MySQLdb()

        user = "root"
        password = "Sangjin<1"
        database = "db_web_project"
        engine = create_engine(f"mysql+mysqldb://{user}:{password}@172.31.21.49:3306/{database}",
                            connect_args={'charset':'utf8mb4'})
        connect = engine.connect

        connect = pymysql.connect(host='172.31.21.49', user='root', password='Sangjin<1', charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        cur = connect.cursor()
        print("connect sql fin in wc")

        query = f"select * from db_web_project.final_review_df where unique_key = '{unique_key}'"
        # create = "create table db_web_project.review_df (UNIQUE_KEY VARCHAR(100), NAME VARCHAR(100), SCORE INT, REVIEW TEXT CHARSET utf8mb4)"
        # set_utf = "ALTER TABLE db_web_project.review_df CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cur.execute(query)
        result = cur.fetchall()
        print(result)
        wrap_bye = [item for item in result[1]]
        print(wrap_bye)
        print("going well wc...44" )
        # cur.execute(create)   
        columns = [column[0] for column in cur.description]
        df = pd.DataFrame(result, columns=wrap_bye)
        # for i in df:
        #     print(i['LABEL'])
        print("going well wc...48" )
        df1 = pd.DataFrame() ## 데이터프래임 생성
#print(df)

        positive = []
        negative = []
        cn=0

        stars=[]
        reviews=[]
        print("going well wc...58" )
        for i,j in zip(df['SCORE'], df['REVIEW']):
        #    i = int(i)
            if int(i)<4: #2.5
                negative.append(j)
            else:
                positive.append(j)     
            cn+=1
            


        font_name = font_manager.FontProperties(fname="malgun.ttf").get_name()

        positive_lst=''

        for i in positive:
            try:
                positive_lst+=i
            except:
                print(0)
                
        negative_lst=''

        for i in negative:
            try:
                negative_lst+=i
            except:
                print(0)

        from konlpy.tag import Okt
        import nltk

        okt = Okt() 

        a = okt.nouns(positive_lst)
        b = nltk.Text(a)
        b = b.vocab().most_common(50)

        c = okt.nouns(negative_lst)
        d = nltk.Text(c)
        d = d.vocab().most_common(50)


        import matplotlib.pyplot as plt
        from wordcloud import WordCloud,STOPWORDS
        ## 긍정적인 워드클라우드 == b 


        if positive_lst:
            file_path = "/home/hadoop/workspace/web/static/star_positive.png"
            os.remove(file_path)

            wordcloud = WordCloud(font_path="malgun.ttf", 
                            stopwords = STOPWORDS, 
                            background_color = "white", 
                            colormap="plasma", 
                            contour_width=0,
                            width =1000 ,height = 800).generate_from_frequencies(dict(b))

            plt.figure(figsize=(5,5))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            wordcloud.to_file("/home/hadoop/workspace/web/static/star_positive.png")
            print("img1 made")
        else:
            pass

        if negative_lst:
            file_path = "/home/hadoop/workspace/web/static/star_negative.png"
            os.remove(file_path)

            wordcloud = WordCloud(font_path="malgun.ttf", 
                            stopwords = STOPWORDS, 
                            background_color = "black", 
                            colormap="plasma", 
                            contour_width=0,
                            width =1000 ,height = 800).generate_from_frequencies(dict(d))

            plt.figure(figsize=(5,5))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            wordcloud.to_file("/home/hadoop/workspace/web/static/star_negative.png")
            print("img2 made")
        else:
            pass

        df1 = pd.DataFrame() ## 데이터프래임 생성
        #print(df)

        positive = []
        negative = []
        cn=0

        stars=[]
        reviews=[]

        for i,j in zip(df['LABEL'], df['REVIEW']):

            if i=="0.0": #2.5
                negative.append(j)
            else:
                positive.append(j)     
            cn+=1
            

        font_name = font_manager.FontProperties(fname="malgun.ttf").get_name()

        positive_lst=''

        for i in positive:
            try:
                positive_lst+=i
            except:
                print(0)
                
        negative_lst=''

        for i in negative:
            try:
                negative_lst+=i
            except:
                print(0)

        from konlpy.tag import Okt
        import nltk

        okt = Okt() 

        a = okt.nouns(positive_lst)
        b = nltk.Text(a)
        b = b.vocab().most_common(50)

        c = okt.nouns(negative_lst)
        d = nltk.Text(c)
        d = d.vocab().most_common(50)


        import matplotlib.pyplot as plt
        from wordcloud import WordCloud,STOPWORDS

        if positive_lst:
            file_path = "/home/hadoop/workspace/web/static/model_positive.png"
            os.remove(file_path)

            wordcloud = WordCloud(font_path="malgun.ttf", 
                            stopwords = STOPWORDS, 
                            background_color = "white", 
                            colormap="cool", 
                            contour_width=0,
                            width =1000 ,height = 800).generate_from_frequencies(dict(b))

            plt.figure(figsize=(5,5))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            wordcloud.to_file("/home/hadoop/workspace/web/static/model_positive.png")
            print("model_positive")
        else:
            pass

        if negative_lst:
            file_path = "/home/hadoop/workspace/web/static/model_negative.png"
            os.remove(file_path)

            wordcloud = WordCloud(font_path="malgun.ttf", 
                            stopwords = STOPWORDS, 
                            background_color = "black", 
                            colormap="cool", 
                            contour_width=0,
                            width =1000 ,height = 800).generate_from_frequencies(dict(d))

            plt.figure(figsize=(5,5))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            wordcloud.to_file("/home/hadoop/workspace/web/static/model_negative.png")
            print("img4 made")
        else:
            pass

        message = 1

    except Exception as e:
        message = 0
    
    return message

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)