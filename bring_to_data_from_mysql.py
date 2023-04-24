import pymysql
import pandas as pd

pymysql.install_as_MySQLdb()

connect = pymysql.connect(host='localhost', user='root', password='1234', charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
cur = connect.cursor()

query = "select * from db_web_project.temp_restaurant_df"
cur.execute(query)

result = cur.fetchall()
connect.close()

df = pd.DataFrame(result)
print(df)