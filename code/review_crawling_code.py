#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from pyvirtualdisplay import Display
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
query = "SELECT * FROM db_web_project.gonggong_original"
cur.execute(query)
result = cur.fetchall()

# Convert query result to a pandas dataframe
first_df = pd.DataFrame(result)

# Display the dataframe
print(first_df)

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
for MGT, name in zip(first_df['UNIQUE_KEY'], first_df['NAME_AND_DONG']):
    df1 = pd.DataFrame()
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
    moreviews = soup.find_all(name="a", attrs={"class":"moreview"})

    # Initialize a list to store the URLs of the restaurants
    urls=["https://place.map.kakao.com/1858663926"]
    st = 0

    # Append the URLs to the list
    for i in moreviews:
        st = 0
        page_url=i.get("href")
        urls.append(page_url)

    # Visit each restaurant URL to extract reviews
    if len(moreviews) >= 1:
        st = 1

    ramen=urls[st]
    driver.get(urls[st])

    try:            
        t1=driver.page_source
        t2=BeautifulSoup(t1, "html.parser")
        place = t2.find('meta', {'name': 'twitter:title'})['content']
    except:
        pass

    # Define the columns for the dataframe
    columns = ['unique_key','name','score', 'review']

    # Initialize lists to store the stars and reviews
    stars=[]
    reviews=[]

    # Get the initial height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to load more reviews
    ctr = True
    while ctr:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Get the new height of the page
        new_height = driver.execute_script("return document.body.scrollHeight")

        # If the height remains the same, exit the loop
        if new_height == last_height:
            break
        last_height = new_height

        # Get the updated page source
        tmp=driver.page_source
        tmp2 = BeautifulSoup(tmp, "html.parser")

        try:
            total_reviews_elem = tmp2.select('#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g')
            reviews_str = total_reviews_elem[0].text.strip()  
            total_reviews = int(re.search(r'\d+', reviews_str).group())
        except:
            break

        # If there are no reviews, exit the loop
        if total_reviews == 0:
            ctr = False
            break

        # Calculate the number of pages to be loaded
        pages = math.ceil(total_reviews/5)
        pages = pages + 1            

        # Load each page and extract the stars and reviews
        for i in range(0, pages):
            try:
                driver.execute_script('return document.querySelector("#mArticle > div.cont_evaluation > div.evaluation_review > a").click()')
            except:
                pass

            time.sleep(2)

        t1 = driver.page_source
        t2 = BeautifulSoup(t1, "html.parser")
        t3 = t2.find(name="div", attrs={"class":"evaluation_review"})

        # Extract the star ratings
        star = t3.find_all('span',{'class':'txt_desc'})

        for j in range(0, len(star)):
            if j%2 != 0:
                lst = star[j]
                stars.extend(lst)

        # Extract the reviews
        review = t3.find_all('p',{'class':'txt_comment'})
        for element in review:
            reviews.append(element.find('span').text)

        # Break the loop if the desired number of pages is loaded
        if i < pages:
            break
        time.sleep(2)

    # Create a dataframe with the extracted stars and reviews
    for s, r in zip(stars, reviews):
        row = [MGT, name, s, r]
        series = pd.Series(row, index=columns)
        df1 = df1._append(series, ignore_index=True)
        df1 = pd.DataFrame(df1)

    # Write the dataframe to the MySQL database
    df1.to_sql(name='review_df', con=engine, if_exists='append', index=False)
    
    # Go back to the search page
    driver.back()

    print(num)
    num = num+1

# Close the database connection
connect.close()
