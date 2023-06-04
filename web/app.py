import requests
from bs4 import BeautifulSoup
from search_mysql import search_mysql_gonggong
import pandas as pd
from four_wordcloud import sickdang_wc
from map_code import on_map
from come_on_menu import menu


from flask import Flask, render_template, request, jsonify, session
app = Flask(__name__)
app.secret_key = 'sangjin'  # session을 위한 비밀키 설정

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/test', methods=['POST'])
def test_get():
    sickdang = request.form.get('sickdang')
    dong = request.form.get('dong')
    print(sickdang, dong)

    session['sickdang'] = sickdang
    session['dong'] = dong
    gonggong = search_mysql_gonggong(sickdang, dong)

    if gonggong['unique_key'] != 0:
        print(gonggong)
        map_bool = on_map(gonggong['unique_key'], sickdang)
        gonggong['have_map'] = map_bool
        if map_bool==1:
            print("complete map")
        wc_bool = sickdang_wc(gonggong['unique_key'])
        print(wc_bool)
        gonggong['have_wc'] = wc_bool

        menu_df = menu(gonggong['name_and_dong'])
        menu_dict = menu_df.to_dict(orient='records')
        print(f"{menu_dict} in app.py")

        gonggong['menus'] = menu_dict
        print("complete menu")
        if wc_bool==1:
            print("complete wc")  

        else:
            print("no wc")

    else:
        print("식당정보를 다시 입력해주십시오")
    

    print("final json")
    print(gonggong)
    return jsonify(gonggong)
    #return jsonify({'result':'success', 'sickdang': sickdang, 'dong':dong})
    #result = f"Received data: sickdang={sickdang}, dong={dong}"
    
    
    # return render_template('index.html')
    



if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)