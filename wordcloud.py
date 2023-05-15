"""
import os

os.system('pip install konlpy')
os.system('pip install nltk')
os.system('pip install matplotlib')
os.system('pip install wordcloud')
"""


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


excel = "C:\\Users\\about\\OneDrive\\바탕 화면\\3_2\\Database Practice Web programming\\Mid\\TeamProJ\\4.29_크롤표본\\business.xlsx"
df = pd.read_excel(excel)

df = pd.DataFrame(df) ## 데이터프래임 생성
df1 = pd.DataFrame() ## 데이터프래임 생성
#print(df)

positive = []
negative = []
cn=0

stars=[]
reviews=[]

for i,j in zip(df['score'], df['review']):
#    i = int(i)
    if int(i)<3.5:
        negative.append(j)
    else:
        positive.append(j)     
    cn+=1

print(cn)
    
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc
from matplotlib import style

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')
labels = ['이상','미만']

frequency = [len(positive),len(negative)]
survey = pd.DataFrame({'frequency':frequency},index = labels)
plt.figure(figsize = (10,10))
survey['frequency'].plot(kind = 'pie',autopct ='%1.1f%%',startangle = 90,colors = ['skyblue','red'],title = '비율',legend = True,fontsize = 15)

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

wordcloud = WordCloud(font_path="c:/Windows/Fonts/malgun.ttf", stopwords = STOPWORDS, background_color = "black", colormap="Blues", width =1000 ,height = 800).generate_from_frequencies(dict(b))

plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
