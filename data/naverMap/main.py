# 네이버 지도 스크래핑
# 네이버 지도는 API를 제공하지만, 요구사항에 적합한 API없음.
# 필요한 속성 Column은 각 검색 결과 객체들의 '이름', '주소', '건축물성격', '준공예정연월' 입니다.

# Request를 반복적으로 날리다보면 CAPCHA화면으로 막히기 떄문에 쿼리 속도를 조절하는 꼼수를 부려야 합니다.
# 헤더없이 python 코드를 실행시키면, 네이버에서 봇 감지를 하여 CAPCHA입력 화면으로 넘어갑니다. 
# Request header 에 브라우저 정보를 강제로 입력하여 봇이 아닌 척 하고 원래 request header에 들어있던 Referer를 그대로 넣도록 하였습니다.

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

pageNum = 1
#year_ = '2023년'
year_ = sys.argv[1] + '년'
url = 'https://map.naver.com/v5/api/search'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Referer': 'https://map.naver.com/',
}

stop_flag = False

while stop_flag == False:
    params = {
        'query': year_,
        'type': 'all',
        'page': pageNum, 
        'isPlaceRecommendationReplace': 'true',
        'lang': 'ko',
        'displayCount': '20',
        'searchCoord': '126.9499895;37.3709175',
    }
    try:
        res = requests.get(url, params=params, headers=header, verify=False)
        data = json.loads(res.text)
        result = data['result']
        search_lists = result['place']['list']
    except Exception as e:
        print(e)
        break

    #print(search_lists)
    print('pageNum: ', pageNum)
    print('len(search_lists): ', len(search_lists))

    if len(search_lists) < 20:
        stop_flag = True

    for i in range(len(search_lists)):
        name_list.append(search_lists[i]['name'].split('(')[0])
        future_list.append(search_lists[i]['name'].split('(')[1][:-1])
        addr_list.append(search_lists[i]['address'])

    pageNum += 1

source = {
    '이름': name_list,
    '준공 예정일': future_list,
    '주소': addr_list,
}

df = pd.DataFrame(source)

#반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
try:
    df.to_excel('C:/JSP/upload/naverMap.xlsx')
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
        curs.execute(sql, ('naverMap.xlsx', 'naverMap.xlsx', 0, formatted_date, 'excel', '100KB'))
    conn.commit()
except Exception as e:
    print(e)
finally:
    conn.close()