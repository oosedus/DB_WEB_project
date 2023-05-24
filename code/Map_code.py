#!/usr/bin/env python
# coding: utf-8

# In[14]:


from sqlalchemy import create_engine
import pymysql
import pandas as pd

pymysql.install_as_MySQLdb()

user = "root"
password = "Sangjin<1"
database = "db_web_project"
engine = create_engine(f"mysql+mysqldb://{user}:{password}@54.252.183.196:3306/{database}",
                     connect_args={'charset':'utf8mb4'})
conn = engine.connect

connect = pymysql.connect(host='54.252.183.196', user='root', password='Sangjin<1', charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
cur = connect.cursor()

query = f"select NAME_AND_DONG, DONG,TYPE from db_web_project.gonggong_original where NAME_AND_DONG = '{name}'"
cur.execute(query)
result = cur.fetchall()

df = pd.DataFrame(result)
Dong = df.at[0, 'DONG']
Type = df.at[0, 'TYPE']

query2 = f"select NAME_AND_DONG, X, Y, AVG_PRICE from db_web_project.location_df where DONG = '{Dong}' and RESTAURANT_TYPE = '{Type}' and X != '' AND Y != ''"

cur.execute(query2)
result2 = cur.fetchall()
df2 = pd.DataFrame(result2)


# In[16]:


df2


# In[12]:


name = input("이름: ")


# In[29]:


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
import math
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

path = 'chromedriver'
source_url = "https://map.kakao.com/"
driver = webdriver.Chrome(path)
driver.get(source_url)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import requests
import folium
import pyproj


map_list = folium.Map(location=[37.566659527,126.978346859], zoom_start=10)


renew_df = pd.DataFrame(df2) ## 데이터프래임 생성


popuplist = []
for (name, average) in zip(renew_df['NAME_AND_DONG'],renew_df['AVG_PRICE']):
    popuplist.append([name, average])


IP = 0

# Iterate over the DataFrame rows
for x, y in zip(renew_df['X'],renew_df['Y']):
    tm = pyproj.Proj(init='epsg:2097')
    wgs84 = pyproj.Proj(init='epsg:4326')
    lat = float(x)
    long = float(y)
    long, lat = pyproj.transform(tm, wgs84, lat, long)

    folium.Marker(
        location=[lat, long],
        popup = popuplist[IP],
        icon=folium.Icon(color='red', icon='glyphicon glyphicon-cutlery')
    ).add_to(map_list)
    IP = IP + 1

# Display the map
map_list


# In[23]:


get_ipython().system('pip install pyproj')


# In[9]:


get_ipython().system('pip install folium')

