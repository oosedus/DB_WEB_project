from flask import Flask, render_template, request, session, jsonify

import mysql.connector


app = Flask(__name__)
app.secret_key = 'sangjin'  # app.py와 동일한 secret_key 값으로 설정

@app.route('/search_mysql')
def search_mysql_gonggong(sickdang, dong):
    #sickdang_web = session.get('sikdang')
    #dong_web = session.get('dong')
    sickdang_web = sickdang
    dong_web = dong
    #print(f"{sickdang_web} {dong_web} moved to search_mysql mehtod!!!")
    
    cnx = mysql.connector.connect(
    host='172.31.21.49',
    user='root',
    password='Sangjin<1',
    database='db_web_project'
    )
    cursor = cnx.cursor()
    cursor.execute('USE db_web_project')
    
    gonggong_columns = ["unique_key", "state", "full_address", "name", "type", "dong", "name_and_dong", "avg_price"]
    sickdang_dict = {}
    try:
        query_gg_original = f"SELECT * FROM gonggong_original WHERE NAME = '{sickdang_web}' AND DONG = '{dong_web}'"
        cursor.execute(query_gg_original)
        gonggong_original_wrap = cursor.fetchall()
        gonggong_original = [item for item in gonggong_original_wrap[0]]
        print(gonggong_original)
        
        for i, gonggong_column in enumerate(gonggong_columns):
            sickdang_dict[gonggong_column] = gonggong_original[i]
        # print(sickdang_dict)
        query_location = f"SELECT X, Y FROM location_df WHERE UNIQUE_KEY = '{sickdang_dict['unique_key']}'"
        cursor.execute(query_location)
        location_wrap = cursor.fetchall()
        # print(location_wrap)
        try:
            location = [item for item in location_wrap[0]]
            # print(location)
            sickdang_dict['x'] = location[0]
            sickdang_dict['y'] = location[1]
        except Exception as e:
            sickdang_dict['x'] = 0
            sickdang_dict['y'] = 0
    except Exception as e:
        for i, gonggong_column in enumerate(gonggong_columns):
            sickdang_dict[gonggong_column] = 0
        sickdang_dict['x'] = 0
        sickdang_dict['y'] = 0
    
    sickdang_dict['have_wc'] = 0
    sickdang_dict['have_map'] = 0
    sickdang_dict['menus'] = 0
  
    cursor.close()
    cnx.close()

    return sickdang_dict

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)