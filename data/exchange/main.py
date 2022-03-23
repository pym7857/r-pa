import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pymysql

# ----------------------- 구리 가격 -----------------------
URL = 'https://markets.businessinsider.com/commodities/copper-price'

req = requests.get(URL, verify=False)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

res = soup.find('div', {"class": "price-section__row"})
copper_info = res.text.replace(" ", "").replace("\n", " ").strip().split(" ")
print(copper_info)

# ----------------------- 은 가격 -----------------------
# [LBMA quandl daily API] am 9:00 업데이트 --> 전 날 가격
url = 'https://www.quandl.com/api/v3/datasets/LBMA/SILVER.json?api_key=Ku_Psp3ffeCg1rJQim3h'

res = requests.get(url, verify=False)
data = json.loads(res.text)
ds = data['dataset']

dataset_code = ds['dataset_code']
database_code = ds['database_code']
refreshed_at = ds['refreshed_at']
newest_available_date = ds['newest_available_date']
column_names = ds['column_names']
frequency = ds['frequency']
silver_info = ds['data'][0]
print(silver_info)

# ----------------------- 환율 -----------------------
# # 환율정보 가져오기(api)
# rate_url = 'https://api.manana.kr/exchange/rate/KRW/KRW,JPY,USD,CNY,EUR.json'
# res = requests.get(rate_url, verify=False)
# data = json.loads(res.text)
# #print(data)

# # 환율정보 가져오기(api)
# rate_url = 'https://api.manana.kr/exchange/rate/USD/EUR.json'
# res2 = requests.get(rate_url, verify=False)
# data2 = json.loads(res2.text)
# #print(data2)

# # 환율정보 가져오기(api)
# rate_url = 'https://api.manana.kr/exchange/rate/JPY/USD.json'
# res3 = requests.get(rate_url, verify=False)
# data3 = json.loads(res3.text)
# #print(data3)

# # 환율정보 가져오기(api)
# rate_url = 'https://api.manana.kr/exchange/rate/CNY/USD.json'
# res4 = requests.get(rate_url, verify=False)
# data4 = json.loads(res4.text)
# #print(data4)



# date_dict = dict()
# value_dict = dict()
# for a in data:
#     date_dict[a['name']] = a['date']
#     value_dict[a['name']] = a['rate']
# #print(date_dict)
# #print(value_dict)

# date_dict2 = dict()
# value_dict2 = dict()
# for a in data2:
#     date_dict2[a['name']] = a['date']
#     value_dict2[a['name']] = a['rate']
# #print(date_dict2)
# #print(value_dict2)

# date_dict3 = dict()
# value_dict3 = dict()
# for a in data3:
#     date_dict3[a['name']] = a['date']
#     value_dict3[a['name']] = a['rate']
# #print(date_dict3)
# #print(value_dict3)

# date_dict4 = dict()
# value_dict4 = dict()
# for a in data4:
#     date_dict4[a['name']] = a['date']
#     value_dict4[a['name']] = a['rate']
# #print(date_dict4)
# #print(value_dict4)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD,FRX.KRWEUR,FRX.KRWJPY,FRX.JPYUSD,FRX.KRWCNY,FRX.CNYUSD'
exchange = requests.get(url, headers=headers).json()
print(len(exchange))

url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWEUR'
exchange2 = requests.get(url, headers=headers).json()
EUR_ = exchange2[0]['basePrice']

url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
exchange3 = requests.get(url, headers=headers).json()
USD_ = exchange3[0]['basePrice']
EUR_USD = round(EUR_/USD_,2)
#print(EUR_USD)



date_list = [exchange[0]['date'] for _ in range(7)]
#print(date_list)

value_list = []
for ex in exchange[:2]:
    value_list.append(ex['basePrice'])
value_list.append(EUR_USD)
for ex in exchange[2:]:
    value_list.append(ex['basePrice'])
#print(value_list)

# date_list.append(date_dict['USDKRW=X'])
# date_list.append(date_dict['EURKRW=X'])
# date_list.append(date_dict2['EURUSD=X'])
# date_list.append(date_dict['JPYKRW=X'])
# date_list.append(date_dict3['USDJPY=X'])
# date_list.append(date_dict['CNYKRW=X'])
# date_list.append(date_dict4['USDCNY=X'])
date_list.append(copper_info[11])
date_list.append(silver_info[0])

# value_list.append(value_dict['USDKRW=X'])
# value_list.append(value_dict['EURKRW=X'])
# value_list.append(value_dict2['EURUSD=X'])
# value_list.append(value_dict['JPYKRW=X']*100)
# value_list.append(value_dict3['USDJPY=X'])
# value_list.append(value_dict['CNYKRW=X'])
# value_list.append(value_dict4['USDCNY=X'])
value_list.append(copper_info[4])
value_list.append(silver_info[1])

print(date_list)
print(value_list)

# index = ['USD/KRW', 'EUR/KRW', 'EUR/USD', '100JPY/KRW', \
#     'USD/JPY', 'CNY/KRW', 'USD/CNY', 'Cu ($/t)', 'Ag ($/oz)']
# source = {
#     '날짜': date_list,
#     '값': value_list,
# }
# df = pd.DataFrame(source, index=index)
# print(df)

# now_date = str(datetime.today()).split(" ")[0]

now_date = str(datetime.today())
df = pd.DataFrame()

try:
    df.to_excel('C:/JSP/upload/exchange.xlsx', index_col=0) # index_col=0 : unnamed error 제거
    print("기존 엑셀 읽어오기 성공")

    try:
        # 기존 df에 새로운 행 추가 
        df.loc[now_date.split(" ")[0]] = [date_list[0], value_list[0], date_list[1], value_list[1], date_list[2], value_list[2], \
            date_list[3], value_list[3], date_list[4], value_list[4], date_list[5], value_list[5], \
                date_list[6], value_list[6], date_list[7], value_list[7], date_list[8], value_list[8]]

        print('기존 df에 새로운 행 추가 완료')
        print(df)
    except Exception as e:
        print(e)
        print('기존 df에 새로운 행 추가 실패')
except Exception as e:
    print(e)
    
    index = [now_date.split(" ")[0]]
    source = {
        '[USD/KRW] 기준일': date_list[0], 
        'USD/KRW': value_list[0], 
        '[EUR/KRW] 기준일': date_list[1],
        'EUR/KRW': value_list[1], 
        '[EUR/USD] 기준일': date_list[2],
        'EUR/USD': value_list[2], 
        '[100JPY/KRW] 기준일': date_list[3],
        '100JPY/KRW': value_list[3],
        '[USD/JPY] 기준일': date_list[4],
        'USD/JPY': value_list[4], 
        '[CNY/KRW] 기준일': date_list[5],
        'CNY/KRW': value_list[5], 
        '[USD/CNY] 기준일': date_list[6],
        'USD/CNY': value_list[6], 
        '[Cu ($/t)] 기준일': date_list[7],
        'Cu ($/t)': value_list[7], 
        '[Ag ($/oz)] 기준일': date_list[8],
        'Ag ($/oz)': value_list[8],
        }
    df = pd.DataFrame(source, index=index)
    print('기존 엑셀 파일이 없습니다.. 새로운 df 생성!')
    print(df)


#반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
try:
    df.to_excel('C:/JSP/upload/exchange.xlsx')
    print('(python code)추출 완료!')
except:
    print('(python code)추출 에러!')
    print('파일이 열려있다면, 반드시 닫아주세요.')

#MySQL과 연동
conn = pymysql.connect(host='localhost', user='root', password='1562', db='file', charset='utf8')

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

try:
    with conn.cursor() as curs:
        sql = """INSERT INTO FILE VALUES (%s, %s, %s, %s, %s, %s)"""
        curs.execute(sql, ('exchange.xlsx', 'exchange.xlsx', 0, formatted_date, 'excel', '100KB'))
    conn.commit()
except Exception as e:
    print(e)
    print('--> 데이터베이스 오류!')
finally:
    conn.close()






# # ----------------------- 환율 -----------------------
# #today = '20210204'
# params = (
#     ('authkey', 'c2qn15XEjGAWtavjI3xQ2Nljkibki5lX'),
#     ('data', 'AP01')
#     #('searchdate', today), # 오늘 날짜 (Default: 현재 날짜)
# )
# # 한국 수출입 은행 OpenAPI (https://www.koreaexim.go.kr/site/program/openapi/openApiView?menuid=001003002002001&apino=2&viewtype=C)
# url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'

# res = requests.get(url, params=params)
# data = json.loads(res.text)

# # 비영업일의 데이터, 혹은 영업당일 11시 이전에 해당일의 데이터를 요청할 경우 null 값이 반환 -> 대안: manana api 쓰기
# # print('환율 = ', data)

# # json 형식의 data
# CNY = data[6] 
# EUR = data[8] 
# JPY = data[12]
# USD = data[-1]

# print('--CNY: ', CNY)
# print('--EUR: ', EUR)
# print('--JPY: ', JPY)
# print('--USD: ', USD)

# print("--검색 요청 날짜: ", datetime.today())



# # ----------------------- 엑셀로 떨구기 -----------------------
# source = {
#     '사업계획': [1180.0, 1309.8, 1.11, 1090.0, 108.26, 169.00, 6.98, 6300.00, 20.00],
#     '19년 연간평균': [1165.4, 1304.5, 112, 1069.4, 108.97, 168.54, 6.91, 6016, 16],
#     '20년 연간평균': [1178.2, 1343.6, 1.14, 1107.5, 106.34, 170.75, 6.90, 6683, 25],
#     '21년 01월 이동환율': [None, None, None, None, None, None, None, None, None],
#     '21년 01월 당월 초순': [None, None, None, None, None, None, None, None, None],
#     '21년 01월 당월 중순': [None, None, None, None, None, None, None, None, None],
#     '21년 01월 21일': [None, None, None, None, None, None, None, None, None],
# }

# df = pd.DataFrame(source, index=['USD/KRW', 'EUR/KRW', 'EUR/USD', '100JPY/KRW', 'USD/JPY', 'CNY/KRW', 'USD/CNY', 'Cu ($/t)', 'Ag ($/oz)'])
# print(df)

# 행/열로 해당 위치 찾기 (이 방법을 권장)
#df.loc['USD/KRW', '21년 01월 21일'] = 99
#print(df)