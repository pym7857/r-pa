import requests
import json 
import pandas as pd 
from datetime import datetime 
import sys 
import pymysql
from time import sleep

name_list = []
future_list = []
addr_list = []

searching = sys.argv[1] + '년'
url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)
headers = {
    "Authorization": "KakaoAK 25c421cf229ad91d4f975c90cf22dfe0",
}

name_list = []
year_list = []
addr_list = []
x_y_list = []

pageNum = 1
stop_flag = False

f = open("새파일.txt", 'w')

while stop_flag==False and pageNum <= 45:
    
    params = {
    'page': pageNum,
    'size': 15,
    }

    try:
        places = requests.get(url, headers=headers, params=params, verify=False).json()['documents']
    except Exception as e:
        print(e)
        break

    if len(places) < 15:
       stop_flag = True

    for place in places:
        name_list.append(place['place_name'].split('(')[0])
        year_list.append(place['place_name'].split('(')[1][:-1])
        addr_list.append(place['address_name'].split('(')[0])

    sleep(10)
    print('10초 휴식 완료')

    pageNum += 1
    print(pageNum)

    try:
        f.write('---\n' + str(pageNum) + '\n' + str(datetime.now()) + '\n')
        f.close()

        f = open(str(pageNum) + "_새파일.txt", 'w')
    except Exception as e:
        print(e)

f.close()

#print(len(name_list))
#print(len(year_list))
#print(len(addr_list))

source = {
    '이름': name_list,
    '준공 예정일': year_list,
    '주소': addr_list,
}

df = pd.DataFrame(source)

#반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
try:
    df.to_excel('C:/JSP/upload/kakaoMap.xlsx')
    print('(python)엑셀 추출 완료!')
except:
    print('(python)엑셀 추출 에러!')
    print('파일이 열려있다면, 반드시 닫아주세요.')

#MySQL과 연동
conn = pymysql.connect(host='localhost', user='root', password='1562', db='file', charset='utf8')

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

try:
    with conn.cursor() as curs:
        sql = """INSERT INTO FILE VALUES (%s, %s, %s, %s, %s, %s)"""
        curs.execute(sql, ('kakaoMap.xlsx', 'kakaoMap.xlsx', 0, formatted_date, 'excel', '100KB'))
    conn.commit()
except Exception as e:
    print(e)
finally:
    conn.close()