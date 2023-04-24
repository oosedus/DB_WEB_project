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

excutable_path = 'chromedriver.exe'
source_url = "https://map.kakao.com/"
driver = webdriver.Chrome(executable_path=excutable_path)

driver.get(source_url)

search=driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')


search.send_keys("아이엠돈까스")
search.send_keys(Keys.ENTER)

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
moreviews = soup.find_all(name="a", attrs={"class":"moreview"})

driver.close()

urls=[]
for i in moreviews:
    page_url=i.get("href")
    urls.append(page_url)
    
ramen=urls[0]

"=============================="

columns = ['score', 'review']
df = pd.DataFrame(columns=columns)

stars=[]
reviews=[]

driver = webdriver.Chrome(executable_path=excutable_path)
driver.get(ramen)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
            
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    tmp=driver.page_source
    tmp2 = BeautifulSoup(tmp, "html.parser")

    total_reviews_elem = tmp2.select('#mArticle > div.cont_evaluation > strong.total_evaluation > span')
    print(total_reviews_elem)
    if len(total_reviews_elem) == 0:
        
        continue

    total_reviews = int(total_reviews_elem[0].get_text())
    

    pages=math.ceil(total_reviews/100)
    print(pages)
    time.sleep(5)

    for i in range(1,pages+1):
        t1=driver.page_source
        t2=BeautifulSoup(t1, "html.parser")
        t3=t2.find(name="div", attrs={"class":"evaluation_review"})

        star=t3.find_all('em',{'class':'num_rate'})
        print("s")
        print(star)
        review=t3.find_all('p',{'class':'txt_comment'})
        print("r")
        print(review)

        stars.extend(star)
        reviews.extend(review)

        if i > pages:
            break
        i=i+1

        driver.execute_script('return document.querySelector("#mArticle > div.cont_evaluation > div.evaluation_review > a").click()')
        time.sleep(2)
        
    for s, r in zip(stars, reviews):
        row = [s.text[0], r.find(name="span").text]
        series = pd.Series(row, index=df.columns)
        df = df.append(series, ignore_index=True)
        
    break
driver.close()



columns = ['score', 'review']
df = pd.DataFrame(columns=columns)

    
df.to_csv('oreno.csv',encoding='utf-8-sig')

