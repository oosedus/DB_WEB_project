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

executable_path = 'chromedriver.exe'
source_url = "https://map.kakao.com/"
driver = webdriver.Chrome(executable_path=executable_path)
driver.get(source_url)

import pandas as pd

excel = "C:\\Users\\about\\OneDrive\\바탕 화면\\3_2\\Database Practice Web programming\\Mid\\TeamProJ\\4.29_크롤표본\\RESU.xlsx"
df = pd.read_excel(excel)
df = pd.DataFrame(df) ## 데이터프래임 생성

for MGT, name, dong in zip(df['MGTNO'],df['NAME'],df['DONG']):
    business = name + " " + dong

    search = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
    search.clear()
    print(business)
    search.send_keys(business)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    # 전체 html
    html = driver.page_source
    # 카카오맵 
    soup = BeautifulSoup(html, "html.parser")
    # a태그에 해당하는 것
    moreviews = soup.find_all(name="a", attrs={"class":"moreview"})
    #urls :: business_names 이름 기준으로 하위로 뻗어나가는 식당들
    urls=[]
    
    for i in moreviews:
        page_url=i.get("href")
        urls.append(page_url)

    # 그 하위로 뻗어나가는 식당 각각를 검색하기    
    try:
        ramen=urls[0]
    except:
        pass
    driver.get(ramen)
                
    t1=driver.page_source
    t2=BeautifulSoup(t1, "html.parser")
    place = t2.find('meta', {'name': 'twitter:title'})['content']
                   
     
    columns = ['MGTNO','name','score', 'review','dong']
#    df = pd.DataFrame(columns=columns)
        
        # 별점과 리뷰 저장공간        
    stars=[]
    reviews=[]

    last_height = driver.execute_script("return document.body.scrollHeight")

        # 스크롤하여 리뷰를 추출하기
    ctr = True
    while ctr:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        tmp=driver.page_source
        tmp2 = BeautifulSoup(tmp, "html.parser")

        total_reviews_elem = tmp2.select('#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g')
        reviews_str = total_reviews_elem[0].text.strip()  

        total_reviews = int(re.search(r'\d+', reviews_str).group())

        if total_reviews == 0:
            ctr = False
            break
    
        pages=math.ceil(total_reviews/5)
        pages = pages + 1            

        for i in range(0,pages):
            try:
                driver.execute_script('return document.querySelector("#mArticle > div.cont_evaluation > div.evaluation_review > a").click()')
            except:
                pass
            
            time.sleep(2)
            
        t1=driver.page_source
        t2=BeautifulSoup(t1, "html.parser")
        t3=t2.find(name="div", attrs={"class":"evaluation_review"})
            
        # 별점 수량
        star=t3.find_all('span',{'class':'txt_desc'})
            
        for j in range(0, len(star)):
            if j%2 != 0:
                lst = star[j]
                stars.extend(lst)
            
        # 각각 리뷰 분석
        review=t3.find_all('p',{'class':'txt_comment'})
        for element in review:
            reviews.append(element.find('span').text)

        if i < pages:
            break
        time.sleep(2)
            
    for s, r in zip(stars, reviews):
        row = [MGT, name, s, r, dong]
                
        series = pd.Series(row, index=columns)
        df = df.append(series, ignore_index=True)

#        df.to_csv(f'{business}.csv', encoding='utf-8-sig', index=False)
        df = pd.DataFrame(df)    

    df = pd.concat([df])

    driver.back()

print(df)
