import requests
from urllib import parse
import pandas as pd
import json
import sys
import pymysql
from datetime import datetime

#######################
#입찰공고 API : 나라장터검색조건에 의한 입찰공고물품조회
#######################

from_date = sys.argv[1]
to_date = sys.argv[2]
target_nm = sys.argv[3]
pred_price = sys.argv[4]

# from_date = '20210401'
# to_date = '20210507'
# target_nm = '전반'
# pred_price = '0'

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
lst_10 = [] # API명

url_list = ['getBidPblancListInfoCnstwkPPSSrch','getBidPblancListInfoServcPPSSrch','getBidPblancListInfoFrgcptPPSSrch','getBidPblancListInfoThngPPSSrch']
#url_list = ['getBidPblancListInfoCnstwkPPSSrch']

for a in url_list:
    url = 'http://apis.data.go.kr/1230000/BidPublicInfoService/' + a
    key = 'kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D'

    print(a)
    try:
        queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode(
            {
            parse.quote_plus('pageNo') : 1, # 필수
            parse.quote_plus('numOfRows') : "100", # 필수
            parse.quote_plus('inqryDiv'): '1', # 필수 (1:공고게시일시, 2:개찰일시)
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
        print('---items---')
        print(items)

        for item in items:

            lst_01.append(str(item['bidNtceNo']) + "-" + str(item['bidNtceOrd']))
            lst_02.append(item['bidNtceNm'])
            try:
                lst_03.append(item['dlvrTmlmtDt'])
            except:
                lst_03.append('없음')

            try:
                lst_04.append(item['bidNtceDt'])
            except:
                lst_04.append('없음')

            try:
                lst_05.append(item['opengDt'])
            except:
                lst_05.append('없음')

            try:
                lst_06.append(item['presmptPrce'])
            except:
                lst_06.append('없음')

            try:
                lst_09.append(item['dminsttNm'])
            except:
                lst_09.append('없음')

            lst_10.append(a)

            ##############################################
            #낙찰정보 API: 조달청_낙찰정보
            ##############################################
            url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusThng' # api doc참조

            #df를 엑셀로 추출
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
                    parse.quote_plus('bidNtceNo'): items['bidNtceNo'], # 공고번호
                    }
                )
                res = requests.get(url + queryParams)
                jsonObject = json.loads(res.text)
                jo = jsonObject.get("response")
                bid_info = jo["body"]["items"][0] # dict

                lst_07.append(bid_info['sucsfbidAmt']) # 실제 낙찰 금액
                lst_08.append(bid_info['bidwinnrNm']) # 계약 업체

            except Exception as e:
                lst_07.append('없음')
                lst_08.append('없음')
                print(e)

    except Exception as e:
        print('here2')
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
        'API명': lst_10,
    }
    print(len(lst_01))
    print(len(lst_02))
    print(len(lst_03))
    print(len(lst_04))
    print(len(lst_05))
    print(len(lst_06))
    print(len(lst_07))
    print(len(lst_08))
    print(len(lst_09))
    print(len(lst_10))

    df = pd.DataFrame(source)

    writer = pd.ExcelWriter('C:/JSP/upload/naraBid.xlsx', engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

    #반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
    try:
        df.to_excel(writer)
        writer.save()
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
