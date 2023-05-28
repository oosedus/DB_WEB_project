import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql

pymysql.install_as_MySQLdb()


# 요청할 API의 기본 URL
base_url = 'http://openapi.seoul.go.kr:8088/'

# API 호출을 위한 요청 파라미터
params = {
    'ServiceKey': '6e69564a7573656134376c56485152',  # 인증키
    'type': 'json',  # 요청 데이터 타입
    'SERVICE': 'LOCALDATA_072404',  # 서비스명
    'START_INDEX': 1,  # 요청 시작 위치
    'END_INDEX': 1000,  # 요청 종료 위치
}

# 전체 데이터를 저장할 리스트
result_list = []

# 전체 데이터 개수
total_count = 0

# 첫 번째 요청 보내기
request_url = f"{base_url}{params['ServiceKey']}/{params['type']}/{params['SERVICE']}/{params['START_INDEX']}/{params['END_INDEX']}/"
response = requests.get(request_url, params=params)
json_data = response.json()

# 전체 데이터 개수 추출
total_count = json_data['LOCALDATA_072404']['list_total_count']
result_list.extend(json_data['LOCALDATA_072404']['row'])

for i in range(1000, total_count+1, 1000):
    result_1000 = []
    # 요청 파라미터 변경
    params['START_INDEX'] = i + 1
    params['END_INDEX'] = i + 1000

    # 요청 보내기
    request_url = f"{base_url}{params['ServiceKey']}/{params['type']}/{params['SERVICE']}/{params['START_INDEX']}/{params['END_INDEX']}/"
    response = requests.get(request_url, params=params)
    json_data = response.json()

    # 데이터 리스트에 저장
    result_1000.extend(json_data['LOCALDATA_072404']['row'])
    print(i)
    #result_1000 = result_list
    user = "root"
    password = "Sangjin<1"
    database = "db_web_project"
    df = pd.DataFrame(result_1000)
    engine = create_engine(f"mysql+mysqldb://{user}:{password}@172.31.21.49:3306/{database}",
                           connect_args={'charset':'utf8'})
    conn = engine.connect
    df.to_sql(name='gonggong_original', con=engine, if_exists='append', index=False)
    engine.dispose()
    print(f"{i}in table gonggong_original")
    #print(f"{result_list.__len__()} in gonggong")

