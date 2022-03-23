# -*- coding: utf-8 -*- 

import xml.etree.ElementTree as ET
import requests
import pandas as pd
import sys
import pymysql
from datetime import datetime

#고유번호 얻기
### 압축파일 안의 xml 파일 읽기
tree = ET.parse('./corp_num/CORPCODE.xml')
root = tree.getroot()

### 회사 이름으로 회사 고유번호 찾기
def find_corp_num(find_name):
    for country in root.iter("list"):
        if country.findtext("corp_name") == find_name:
            return country.findtext("corp_code")

# 사용자 입력 부분 
#CORP_NAME = '효성중공업'
CORP_NAME = sys.argv[3].replace(" ", "").strip() # 띄어쓰기 및 양쪽 공백제거

try:
    corp_code = find_corp_num(CORP_NAME)
    print(corp_code)
except Exception as e:
    print(e)
    print('해당 회사 명이 없습니다.')


#https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml?crtfc_key=5f1d10ac04bc83ed14b340b5a39a0418bd0261c6&corp_code=01205851&bsns_year=2019&reprt_code=11014&fs_div=CFS
#단일회사 전체 재무제표 API
url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml' # xml로 가져옵니다.

# 사용자 입력 부분 2
YEAR = sys.argv[1]
CODE = sys.argv[2]
# YEAR = '2019'
# CODE = '11014' # 1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011

params = (
    ('crtfc_key', '5f1d10ac04bc83ed14b340b5a39a0418bd0261c6'), # 인증키 
    ('corp_code', str(corp_code)),
    ('bsns_year', YEAR),
    ('reprt_code', CODE), 
    ('fs_div', 'CFS') # CFS:연결재무제표, OFS:재무제표
)

res = requests.get(url, params=params)
print('res.text= \n', res.text) # xml

tree = ET.ElementTree(ET.fromstring(res.text))
root = tree.getroot()


classification_list = []
try:
    for i in root.iter('sj_nm'): # 재무제표 명
        classification_list.append(i.text)
except:
    classification_list = [None]*len(need_accnt_list)

accnt_list = []
try:
    for i in root.iter('account_nm'): # 계정명
        accnt_list.append(i.text)
except:
    accnt_list = [None]*len(need_accnt_list)

price_list = []
try:
    for i in root.iter('thstrm_amount'): # 당기금액
        if (type(i.text) == str):
            price_list.append(format(int(i.text), ","))
        else:
            price_list.append(i.text)
except:
    price_list = [None]*len(need_accnt_list)

period_list = []
try:
    for i in root.iter('thstrm_nm'): # 당기명
        period_list.append(i.text)
except:
    period_list = [None]*len(need_accnt_list)



source = { # columns
    '재무제표명': classification_list,
    '당기명': period_list,
    CORP_NAME: price_list,
}
df = pd.DataFrame(source, index=accnt_list)
print(df)
#print(df.loc['유동자산'][CORP_NAME]) # 가격이 나옴

try:
    df.to_excel('C:/JSP/upload/dart.xlsx')
    print('(python)추출 완료!')
except Exception as e:
    print(e)
    print('(python)추출 에러!')
    print('파일이 열려있다면, 반드시 닫아주세요.')

#MySQL과 연동
conn = pymysql.connect(host='localhost', user='root', password='1562', db='file', charset='utf8')

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

try:
    with conn.cursor() as curs:
        sql = """INSERT INTO FILE VALUES (%s, %s, %s, %s, %s, %s)"""
        curs.execute(sql, ('dart.xlsx', 'dart.xlsx', 0, formatted_date, 'excel', '100KB'))
    conn.commit()
except Exception as e:
    print(e)
finally:
    conn.close()










# try:
#     df.to_excel('result.xlsx')
#     print('엑셀 추출 성공!')
# except:
#     print('엑셀 추출 실패!')






#최종 excel 추출 형태 (구조)

#-BSCF: (API)재무 상태표
#   - [자산]: (API)자산총계
#   - [부채]: (API)부채총계
#   - [부채]유동부채: (API)유동부채
#   - [부채]비유동부채: (API)비유동부채
#   - [부채]차입금: 단기 + 장기
#   - [부채](단기): (API)단기금융부채
#   - [부채](장기): (API)장기금융부채
#   - [자본]: (API)자본총계
#   - [부채비율]: (API)부채/자본 을 계산
#   - [차입금비율]: (API)차입금/자본 을 계산
#-실적관리용: (API)포괄손익계산서
#   - 매출: (API)매출액
#   - 매출이익: (API)매출총이익
#   - 영업이익: (API)영업이익(손실)
#   - 당기순이익: (API)법인세비용차감전순이익(손실)
#   - 중공업, 건설: (효성 중공업 홈페이지 에서..)
#-Cashflow: (API)현금흐름표
#   - 영업: (API)영업활동으로 인한 순현금흐름
#   - 투자: (API)투자활동으로 인한 순현금흐름
#   - 재무: (API)재무활동으로 인한 순현금흐름
#   - 분기말의현금및현금성자산: (API)분기말의 현금및현금성자산

# source = { # columns
#     '구분': ['BSCF', 'BSCF', 'BSCF', 'BSCF', '실적관리용', '실적관리용', '실적관리용', '실적관리용', 'Cashflow', 'Cashflow', 'Cashflow', 'Cashflow'],
#     '현대일렉트릭': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], # dummy data
#     '효성중공업': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
# }

# df = pd.DataFrame(source, index=['유동자산', '비유동자산', '유동부채', '비유동부채', \
#     '매출액', '메출총이익', '영업이익', '법인세비용차감전순이익', '영업', '투자', '재무', '분기말의현금및현금성자산'])
# print(df)

# # df 삽입 : df.loc['row이름', '컬럼이름']

# df.to_excel('result.xlsx')