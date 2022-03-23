import streamlit as st
import pandas as pd
import datetime
import json
import requests
import pandas as pd
from urllib import parse
from st_aggrid import AgGrid

def bid():

    sidebar = st.sidebar
    sidebar.header("Settings")

    from_date = sidebar.date_input(
        "시작날짜",
        datetime.date(2022, 1, 1)
    )
    to_date = sidebar.date_input(
        "종료날짜",
        datetime.date(2022, 1, 2)
    )
    target_nm = sidebar.text_input('검색어', '전반')
    pred_price = sidebar.text_input('가격', 1)

    from_date = str(from_date)
    to_date = str(to_date)
    from_date = from_date.split("-")[0] + from_date.split("-")[1] + from_date.split("-")[2]
    to_date = to_date.split("-")[0] + to_date.split("-")[1] + to_date.split("-")[2]

    if st.button("실행"):
        with st.spinner("wait.."):
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
            #lst_07 = [] # 실제낙찰금액 (낙찰 페이지)
            #lst_08 = [] # 계약업체 (낙찰 페이지)
            lst_09 = [] # 수요기관
            lst_10 = [] # API명

            url_list = ['getBidPblancListInfoCnstwkPPSSrch','getBidPblancListInfoServcPPSSrch','getBidPblancListInfoFrgcptPPSSrch','getBidPblancListInfoThngPPSSrch']
            #url_list = ['getBidPblancListInfoCnstwkPPSSrch']

            idx = 25
            for a in url_list:
                st.write(f"(추출중) {idx}% 추출 완료..")
                idx += 25
                url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/' + a
                key = 'kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D'

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
                    '수요기관': lst_09,
                    'API명': lst_10,
                }
                print(len(lst_01))
                print(len(lst_02))
                print(len(lst_03))
                print(len(lst_04))
                print(len(lst_05))
                print(len(lst_06))
                print(len(lst_09))
                print(len(lst_10))

                df = pd.DataFrame(source)

                if a == 'getBidPblancListInfoThngPPSSrch':
                    AgGrid(df)

            # 엑셀로 추출
            try:
                df.to_excel('./naraBid.xlsx')
                st.write("(엑셀)추출 완료!")
            except Exception as e:
                st.write(e)
                
            with open("naraBid.xlsx", "rb") as file:
                btn = st.download_button(
                        key="naraBid.xlsx,",
                        label="Download Excel",
                        data=file,
                        file_name="naraBid.xlsx",
                        mime="application/vnd.ms-excel"
                )
