import requests
from urllib import parse
import pandas as pd
import json
import sys
import pymysql
from datetime import datetime

#######################
#입찰공고 API
#######################

from_date = sys.argv[1]
to_date = sys.argv[2]
target_nm = sys.argv[3]
pred_price = sys.argv[4]

# from_date = '2020-01-01'
# to_date = '2020-01-31'
# target_nm = '전반'
# pred_price = '300000000'

url = 'http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoThngPPSSrch' # api doc참조
key = 'kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D'

try:
    i = 0
    total = []

    while True:
        i += 1
        print(i)
        queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode(
            {
            parse.quote_plus('pageNo') : i, # 필수
            parse.quote_plus('numOfRows') : "100", # 필수
            parse.quote_plus('inqryDiv'): '1', # 필수 (검색하고자하는 조회구분 1.등록일시, 2.입찰공고번호 3.변경일시)
            parse.quote_plus('inqryBgnDt'): from_date, # 검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
            parse.quote_plus('inqryEndDt'): to_date, # 검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
            parse.quote_plus('type'): 'json', # 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정
            parse.quote_plus('bidNtceNm'): target_nm,
            parse.quote_plus('presmptPrceBgn'): pred_price, #추정금액 3억원 이상
            }
        )
        res = requests.get(url + queryParams)
        jsonObject = json.loads(res.text)
        jo = jsonObject.get("response")
        items = jo["body"]["items"]

        if len(items) <= 0:
            break

        #total.append(items) # 이 형태로 하면 X
        total = total + items # 배열 더하기

except Exception as e:
    print(e)

# ▶조달청_입찰공고정보 API
# [공고일반]
# 입찰공고번호: bidNtceNo + bidNtceOrd
# 공고명: bidNtceNm
# 게시일시: bidNtceDt
# 수요기관: dminsttNm

# [입찰집행 및 진행 정보]
# 개찰(입찰)일시: opengDt

# [예정가격 결정 및 입찰금액 정보]
# 추정가격: presmptPrce

# [구매 대상 물품]
# 납품기한: dlvrTmlmtDt

print('총' + str(len(total)) + '개의 공고를 찾았습니다.')
#print(items) # [{}, {}, {}]

# ▶client 요청 형식
lst_01 = [] # 공고번호
lst_02 = [] # 공고명
lst_03 = [] # 납기(일자)
lst_empty_01 = []
lst_empty_02 = []
lst_empty_03 = []
lst_empty_04 = []
lst_empty_05 = []
lst_04 = [] # 게시일자
lst_05 = [] # 개찰일자
lst_06 = [] # 추정금액
lst_07 = [] # 실제낙찰금액 (낙찰 페이지)
lst_08 = [] # 계약업체 (낙찰 페이지)
lst_09 = [] # 수요기관

#######################
#낙찰정보 API
#######################
url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusThng' # api doc참조
key = 'kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D'

#df를 엑셀로 추출
for item in total:
    try:
        #공고번호가 "개찰완료"인 상태만 기록한다.
        queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode(
            {
            parse.quote_plus('pageNo') : '1', # 필수
            parse.quote_plus('numOfRows') : '100', # 필수
            parse.quote_plus('inqryDiv'): '4', # 필수 (1.등록일시, 2.공고일시,3.개찰일시, 4.입찰공고번호)
            #parse.quote_plus('inqryBgnDt'): '202101190000', # 검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
            #parse.quote_plus('inqryEndDt'): '202102172359', # 검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
            parse.quote_plus('type'): 'json', # 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정
            parse.quote_plus('bidNtceNo'): item['bidNtceNo'], # 공고번호
            }
        )
        res = requests.get(url + queryParams)
        jsonObject = json.loads(res.text)
        jo = jsonObject.get("response")
        bid_info = jo["body"]["items"][0] # dict

        lst_01.append(str(item['bidNtceNo']) + "-" + str(item['bidNtceOrd']))
        lst_02.append(item['bidNtceNm'])
        lst_03.append(item['dlvrTmlmtDt'])
        lst_04.append(item['bidNtceDt'])
        lst_05.append(item['opengDt'])
        lst_06.append(item['presmptPrce'])
        lst_07.append(bid_info['sucsfbidAmt']) # 실제 낙찰 금액
        lst_08.append(bid_info['bidwinnrNm']) # 계약 업체
        lst_09.append(item['dminsttNm'])
    except Exception as e:
        print('here')
        print(e)

#######################
#최종 df추출
#######################

lst_empty_01 = [None]*len(lst_01)
lst_empty_02 = [None]*len(lst_01)
lst_empty_03 = [None]*len(lst_01)
lst_empty_04 = [None]*len(lst_01)
lst_empty_05 = [None]*len(lst_01)

source = {
    '공고번호': lst_01,
    '공고명': lst_02,
    '납기(일자)': lst_03,
    '현장 담당자': lst_empty_01,
    '현장': lst_empty_02,
    '특약점 담당자': lst_empty_03,
    '거래특약점': lst_empty_04,
    '진행현황': lst_empty_05,
    '게시일자': lst_04,
    '개찰일자': lst_05,
    '추정금액': lst_06,
    '실제낙찰금액': lst_07,
    '계약업체': lst_08,
    '수요기관': lst_09,
}
df = pd.DataFrame(source)
print(df)

#반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
try:
    df.to_excel('C:/JSP/upload/naraBid.xlsx')
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
        curs.execute(sql, ('naraBid.xlsx', 'naraBid.xlsx', 0, formatted_date, 'excel', '100KB'))
    conn.commit()
except Exception as e:
    print(e)
finally:
    conn.close()

