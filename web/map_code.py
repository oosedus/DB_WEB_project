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

@app.route('/get_map_data')
def on_map(unique_key, sickdang_name):

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
        print("connect sql fin in map")

        query = f"select NAME_AND_DONG, DONG,TYPE from db_web_project.gonggong_original where UNIQUE_KEY = '{unique_key}'"
            # create = "create table db_web_project.review_df (UNIQUE_KEY VARCHAR(100), NAME VARCHAR(100), SCORE INT, REVIEW TEXT CHARSET utf8mb4)"
            # set_utf = "ALTER TABLE db_web_project.review_df CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cur.execute(query)
        result = cur.fetchall()
        print(f"\n\n\n\{result}\n\n\n")
        wrap_bye = [item for item in result[0]]
        #print(wrap_bye)
        print("going well map...44" )

        
        df = pd.DataFrame(result, columns=wrap_bye)
        print(df)

        Dong = df.at[0, 'DONG']
        Type = df.at[0, 'TYPE']

        query2 = f"select NAME_AND_DONG, X, Y, AVG_PRICE from db_web_project.location_df where DONG = '{Dong}' and RESTAURANT_TYPE = '{Type}' and X != '' AND Y != ''"

        cur.execute(query2)
        result2 = cur.fetchall()
        #print(result2)
        wrap_bye2 = [item for item in result2[0]]
        #print(wrap_bye2)
        print("going well map...44" )
        # cur.execute(create)   
        
        df2 = pd.DataFrame(result2, columns=wrap_bye2)
        print(df2)
            # for i in df:
            #     print(i['LABEL'])
        print("going well map...51" )

        display = Display(visible=0, size=(700, 600))
        display.start()

        path = 'chromedriver'
        source_url = "https://map.kakao.com/"
        driver = webdriver.Chrome(path)
        driver.get(source_url)

        map_list = folium.Map(location=[37.566659527,126.978346859], zoom_start=12)
        renew_df = pd.DataFrame(df2) ## 데이터프래임 생성
        print(renew_df)

        popuplist = []
        for (name, average) in zip(renew_df['NAME_AND_DONG'],renew_df['AVG_PRICE']):
            popuplist.append([name, average])
    
        font_path = '/home/hadoop/workspace/web/malgun.ttf'  # 사용하고자 하는 폰트 경로로 변경해주세요
        font_prop = font_manager.FontProperties(fname=font_path)
        
        sorted_data = sorted(zip(renew_df['NAME_AND_DONG'], renew_df['AVG_PRICE']), key=lambda x: x[1])

        # x, y 데이터 추출
        x_values = [data[0] for data in sorted_data]
        y_values = [data[1] for data in sorted_data]

        

        # Bar plot 그리기
        plt.figure(figsize=(40, 5))
        plt.rcParams['font.size'] = 35
        plt.bar(x_values, y_values, color=['red' if name == sickdang_name else 'blue' for name in x_values])

        # x축 레이블 및 각도 설정 (옵션)
        # plt.xticks(rotation=0, fontproperties=font_prop, ha='right', fontsize=15)

        indices = np.arange(len(x_values))
        selected_indices = [i for i, name in enumerate(x_values) if name == sickdang_name]
        plt.xticks(indices[selected_indices], np.array(x_values)[selected_indices],fontsize=35,fontproperties=font_prop)

        for x_value, y_value in zip(x_values, y_values):
            if x_value == sickdang_name:
                plt.annotate(str(y_value), (x_value, y_value), ha='center', va='bottom')

        # 그래프 제목 설정 (옵션)
        

        plt.title('Average Price by town and type')

        # 그래프 저장
        plt.savefig('/home/hadoop/workspace/web/static/bar_plot.png', dpi=200)



        IP = 0

        # # Create figure and axes
        # fig, ax = plt.subplots()

        # # Iterate over the DataFrame rows
        # for index, row in df2.iterrows():
        #     # CRS 생성
        #     crs_wgs84 = CRS("EPSG:4326")  # WGS84 CRS
        #     crs_tm = CRS("EPSG:5179")  # TM CRS, 이 값은 실제 CRS에 따라 변경해야 할 수 있습니다.

        #     # Transformer 생성
        #     transformer = Transformer.from_crs(crs_tm, crs_wgs84)

        #     # 좌표 변환
        #     lat = float(row['X'])
        #     long = float(row['Y'])
        #     long, lat = transformer.transform(lat, long)

        #     # Plot the transformed coordinates
        #     ax.scatter(long, lat, color='red')

        # # Get the map as an HTML string
        # map_html = mplleaflet.fig_to_html(fig)

        # return render_template('index.html', map_html=map_html)

        # Iterate over the DataFrame rows
        # for x, y in zip(renew_df['X'],renew_df['Y']):
        #     # CRS 생성
        #     crs_wgs84 = CRS("EPSG:4326")  # WGS84 CRS
        #     crs_tm = CRS("EPSG:5179")  # TM CRS, 이 값은 실제 CRS에 따라 변경해야 할 수 있습니다.

        #     # Transformer 생성
        #     transformer = Transformer.from_crs(crs_tm, crs_wgs84)

        #     # 좌표 변환
        #     lat = float(x)
        #     long = float(y)
        #     long, lat = transformer.transform(lat, long)

        #     # tm = pyproj.Proj(init='epsg:2097')
        #     # wgs84 = pyproj.Proj(init='epsg:4326')
        #     # lat = float(x)
        #     # long = float(y)
        #     # long, lat = pyproj.transform(tm, wgs84, lat, long)

        #     folium.Marker(
        #         location=[lat, long],
        #         popup = popuplist[IP],
        #         icon=folium.Icon(color='red', icon='glyphicon glyphicon-cutlery')
        #     ).add_to(map_list)
        #     IP = IP + 1

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

        # Folium 객체를 HTML 문자열로 변환
            
        map_list.save('/home/hadoop/workspace/web/static/map.html')

        
        message = 1
        

    except Exception as e:
        message = 0
    
    return message


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)