from sqlalchemy import create_engine
import pymysql
import pandas as pd
from flask import Flask, render_template, request, session, jsonify
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import folium
import pyproj
from pyproj import CRS, Transformer
from pyppeteer import launch
import matplotlib.pyplot as plt
from matplotlib import font_manager
import mplleaflet
import numpy as np

app = Flask(__name__)
app.secret_key = 'sangjin'  # app.py와 동일한 secret_key 값으로 설정

@app.route('/menu')
def menu(name_and_dong):
    #sickdang_web = session.get('sikdang')
    #dong_web = session.get('dong')
    
    #print(f"{sickdang_web} {dong_web} moved to search_mysql mehtod!!!")
    
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
        print("connect sql fin in menu")
        print(name_and_dong)
       
        # create = "create table db_web_project.review_df (UNIQUE_KEY VARCHAR(100), NAME VARCHAR(100), SCORE INT, REVIEW TEXT CHARSET utf8mb4)"
        # set_utf = "ALTER TABLE db_web_project.review_df CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        query = f"select  MENU, PRICE from db_web_project.menu_df where NAME_AND_DONG = '{name_and_dong}'"
        cur.execute(query)
        result = cur.fetchall()
        print(result)
        df1 = pd.DataFrame(result)
        print(df1)
        print(type(df1))

        return df1

    except Exception as e:
        return 0







if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)