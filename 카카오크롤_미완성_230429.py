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

#business_names = ['가마치 통닭(독립문역점)','마우디 브런치 바 (Maudie Brunch Bar)','삼포집','망원 술집','마추픽추(machu picchu)']
business_names = ['아이엠돈까스','삼포집']

# for business in business_names: 식당 리스트를 순서대로 검색하기
for business in business_names:
    search = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
    search.clear()
    print(business)
    search.send_keys("서울 "+business)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    moreviews = soup.find_all(name="a", attrs={"class":"moreview"})

    #urls :: business_names 이름 기준으로 하위로 뻗어나가는 식당들
    urls=[]
    for i in moreviews:
        page_url=i.get("href")
        urls.append(page_url)
        
    # 그 하위로 뻗어나가는 식당 각각를 검색하기    
    for i in range(len(urls)):
        ramen=urls[i]
        print(ramen)
        driver.get(ramen)
        
        # 각각의 하위 식당 저장공간
        p = []
        p = urls[i]
        
        columns = ['place','score', 'review']
        df = pd.DataFrame(columns=columns)
        
        # 별점과 리뷰 저장공간        
        stars=[]
        reviews=[]

        last_height = driver.execute_script("return document.body.scrollHeight")

        # 스크롤하여 리뷰를 추출하기
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
            if len(total_reviews_elem) == 0:
                continue

            total_reviews = int(total_reviews_elem[0].get_text())

            # 축출할 리뷰범위 조정가능 :: 5 -> 1로 변경 시 더 많은 리뷰를 끌어옴
            pages=math.ceil(total_reviews/5)
            
            # 리뷰 페이지 범위
            for i in range(1,pages+1):
                t1=driver.page_source
                t2=BeautifulSoup(t1, "html.parser")
                t3=t2.find(name="div", attrs={"class":"evaluation_review"})
            
                star=t3.find_all('span',{'class':'txt_desc'})
                for i in range(0, len(star)):
                    if i%2 != 0:
                        lst = star[i]
                        stars.extend(lst)
                    
                review=t3.find_all('p',{'class':'txt_comment'})
                for element in review:
                    reviews.append(element.find('span').text)
                        
                if i > pages:
                    break
                i=i+1
                time.sleep(2)

                # 더보기 클릭 버튼 더보기가 없다면 pass
                try:
                    driver.execute_script('return document.querySelector("#mArticle > div.cont_evaluation > div.evaluation_review > a").click()')
                except:
                    pass

                time.sleep(2)

                df = pd.DataFrame(columns=columns)
            
            # 장소, 별점, 리뷰 : 차례로 저장
            for s, r in zip(stars, reviews):
                row = [p, s, r]
                
                print("row")
                print(row)
                
                series = pd.Series(row, index=columns)
                df = df.append(series, ignore_index=True)
            df.to_csv(f'{business}.csv', encoding='utf-8-sig', index=False)
        driver.back()

# 목표 엑셀에 식당명까지 포함하고 하나의 파일로 합치기 
# 결과 :: 중복없음


