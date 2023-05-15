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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import requests
import folium


map_list = folium.Map(location=[37.566659527,126.978346859], zoom_start=10)



excel = "C:\\Users\\about\\OneDrive\\바탕 화면\\3_2\\Database Practice Web programming\\Mid\\TeamProJ\\4.29_크롤표본\\RESU_PRI.xlsx"
df = pd.read_excel(excel)

df = pd.DataFrame(df) ## 데이터프래임 생성
df1 = pd.DataFrame() ## 데이터프래임 생성

########################################
df2 = pd.DataFrame() ## 데이터프래임 생성
########################################


popuplist = []


for MGT, name, dong in zip(df['MGTNO'],df['BPLCNM'],df['dong']):
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
                   
     
    columns = ['MGTNO','name','menu','price']
    
    avg_columns = ['MGTNO','name','average']

        # 별점과 리뷰 저장공간        
    menu=[]
    price=[]
    
    ################
    avg_pri_arr = []
    
    ################

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

        result = tmp2.select('#mArticle > div.cont_menu > ul > li')
        
        for i in range(1,len(result)+1):

            tit_0 = tmp2.select('#mArticle > div.cont_menu > ul > li:nth-child('+str(i)+') > div > span')

            tit_0_text = tit_0[0].text
            menu.append(tit_0_text)
            
            tit = tmp2.select('#mArticle > div.cont_menu > ul > li:nth-child('+str(i)+') > div > em.price_menu')
            #print(tit)
            tit_text = tit[0].text.split(": ")[1]
            #print(tit_text)
            
            price.append(tit_text)

        ###############################
        # 평균가격
        summ = 0
        converted_array = []

        for num in price:
            num = int(num.replace(',', ''))
            converted_array.append(num)
        
        for pr in converted_array:
            summ += pr;
            
        avg_pri = int(summ / len(result))
        print("avg_pri")            
        print(avg_pri)

        
        avg_pri_arr.append(avg_pri)
        ###############################
    
    ###############################
    for avg in zip(avg_pri_arr):

        avg_row = [MGT, name, avg]
                    
        series = pd.Series(avg_row, index=avg_columns)

        df2 = df2.append(series, ignore_index=True)
        df2 = pd.DataFrame(df2)    

    df2 = pd.concat([df2])

    # 수정사항1 : append, concat는 주피터에 있는 구조와 다르니 추후에 다시 확인
    # 수정사항2 : 가격이 null일때 제외하는 상황을 포함하지 않음
    driver.back()

for (name, average) in zip(df2['name'],df2['average']):
    popuplist.append([name, average])
    #driver.back()
print(popuplist)
    



latitude = [37.48572479,
37.54418847,
37.51140929
]
longtitude = [126.8964296,
127.0701207,
127.0582048
]

for i in range(3):
    lat = float(latitude[i])
    long = float(longtitude[i])
    folium.Marker(
        location = [lat, long],
        popup = popuplist[i],
        icon=folium.Icon(color='red', icon='glyphicon glyphicon-cutlery')
    ).add_to(map_list)
map_list

