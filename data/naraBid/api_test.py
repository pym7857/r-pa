import requests
from urllib import parse
import pandas as pd
import json

######################
#입찰공고 API
#######################
url = 'http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoThngPPSSrch' # api doc참조
key = 'kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D'

# TODO: 조회검색 날짜 text파일로 input받기로 수정하기
queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode({
    parse.quote_plus('pageNo') : '1', # 필수
    parse.quote_plus('numOfRows') : '100', # 필수
    parse.quote_plus('inqryDiv'): '1', # 필수 (검색하고자하는 조회구분 1.등록일시, 2.입찰공고번호 3.변경일시)
    parse.quote_plus('inqryBgnDt'): '202102030000', # 검색하고자하는 등록일시 또는 변경일시 조회시작일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
    parse.quote_plus('inqryEndDt'): '202103042359', # 검색하고자하는 등록일시 또는 변경일시 조회종료일시 "YYYYMMDDHHMM", (조회구분 '1' 선택시 필수)
    parse.quote_plus('type'): 'json', # 오픈API 리턴 타입을 JSON으로 받고 싶을 경우 'json' 으로 지정
    parse.quote_plus('bidNtceNm'): '전반',
    parse.quote_plus('presmptPrceBgn'): '300000000', #추정금액 3억원 이상
})

res = requests.get(url + queryParams)
print(res.text)
jsonObject = json.loads(res.text)
jo = jsonObject.get("response")
items = jo["body"]["items"]
print('총' + str(len(items)) + '개의 공고를 찾았습니다.')

