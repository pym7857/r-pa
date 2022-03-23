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

from_date = '20210401'
to_date = '20210507'
target_nm = '전반'
pred_price = '300000000'

url_list = ['getBidPblancListInfoCnstwkPPSSrch','getBidPblancListInfoServcPPSSrch','getBidPblancListInfoFrgcptPPSSrch','getBidPblancListInfoThngPPSSrch']
#url_list = ['getBidPblancListInfoCnstwkPPSSrch']

for a in url_list:
    url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/' + a
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
        print(res)
        print(res.text)
    except Exception as e:
        print(e)