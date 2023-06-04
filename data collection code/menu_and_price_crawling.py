#!/usr/bin/env python
# coding: utf-8

# Import required libraries
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
import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from pyvirtualdisplay import Display

# Connect to MySQL database
pymysql.install_as_MySQLdb()
user = "root"
password = "Sangjin<1"
database = "db_web_project"
engine = create_engine(f"mysql+mysqldb://{user}:{password}@172.31.21.49:3306/{database}",
                       connect_args={'charset':'utf8mb4'})
conn = engine.connect()

# Connect to MySQL database using pymysql
connect = pymysql.connect(host='172.31.21.49', user='root', password='Sangjin<1', charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
cur = connect.cursor()

# Query to fetch Seoul restaurant data from MySQL
query = "SELECT distinct UNIQUE_KEY, NAME FROM db_web_project.review_df"
cur.execute(query)
result = cur.fetchall()

# Convert query result to a pandas dataframe
first_df = pd.DataFrame(result)

# Set up a virtual display
display = Display(visible=0, size=(1024, 768))
display.start()

# Set the path for the Chrome webdriver
path = 'chromedriver'

# URL for Kakao Maps
source_url = "https://map.kakao.com/"

# Launch the Chrome webdriver
driver = webdriver.Chrome(path)
driver.get(source_url)


# Iterate over the rows of the dataframe
for MGT, name in zip(first_df['UNIQUE_KEY'], first_df['NAME']):
    df1 = pd.DataFrame()
    menu = []
    price = []
    
    business = name

    # Search for the restaurant on Kakao Maps
    search = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
    search.clear()
    print(business)
    search.send_keys(business)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    # Get the HTML source of the page
    html = driver.page_source

    # Parse the HTML source using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Find the "moreview" links on the page
    moreviews = soup.find_all(name="a", attrs={"class": "moreview"})

    # Initialize a list to store the URLs of the restaurants
    urls = []

    # Append the URLs to the list
    for i in moreviews:
        page_url = i.get("href")
        urls.append(page_url)

    try:
        ramen = urls[0]
    except:
        pass
    driver.get(ramen)

    # Get the HTML source of the page
    t1 = driver.page_source

    # Parse the HTML source using BeautifulSoup
    t2 = BeautifulSoup(t1, "html.parser")

    # Find the place name
    place = t2.find('meta', {'name': 'twitter:title'})['content']

    # Define the columns for the dataframe
    columns = ['UNIQUE_KEY', 'NAME_AND_DONG', 'MENU', 'PRICE']

    last_height = driver.execute_script("return document.body.scrollHeight")

    ctr = True
    while ctr:
        # Scroll down to load more menu items
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Get the new height of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # If the height remains the same, exit the loop
        if new_height == last_height:
            break
            
        last_height = new_height

        # Get the updated HTML source of the page
        tmp = driver.page_source
        tmp2 = BeautifulSoup(tmp, "html.parser")
        
        # Extract the menu items and prices
        result = tmp2.select('#mArticle > div.cont_menu > ul > li')

        for i in range(1, len(result) + 1):
            tit_0 = tmp2.select('#mArticle > div.cont_menu > ul > li:nth-child(' + str(i) + ') > div > span')
            tit_0_text = tit_0[0].text
            menu.append(tit_0_text)

            tit = tmp2.select('#mArticle > div.cont_menu > ul > li:nth-child(' + str(i) + ') > div > em.price_menu')
            
            # Break the loop if there are no prices
            if len(tit) == 0:
                break
                
            tit_text = tit[0].text.split(": ")[1]
            price.append(tit_text)

        if len(price) == 0:
            continue
            
        # Create a dataframe with the extracted menu items and prices
        for s, r in zip(menu, price):
            row = [MGT, name, s, r]
            series = pd.Series(row, index=columns)
            df1 = df1._append(series, ignore_index=True)
            df1 = pd.DataFrame(df1)

        # Write the dataframe to the MySQL database
        df1.to_sql(name='menu_df', con=engine, if_exists='append', index=False)

        try:
            price = [int(x.replace(',', '')) for x in price]
        except:
            continue

        # Calculate the average price
        if(type(price[0]) == int):
            total_sum = sum(price)
            avg = int(total_sum/len(price))
            
            # Update the average price in the original table
            add_price = f"UPDATE db_web_project.gonggong_original SET AVG_PRICE = \
                {avg} WHERE UNIQUE_KEY = '{MGT}'"
            cur.execute(add_price)

    # Go back to the search page
    driver.back()

# Close the database connection
connect.close()
