import streamlit as st
import pandas as pd
import datetime
import json
import requests
import pandas as pd
from urllib import parse
from st_aggrid import AgGrid

def contract():

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

    from_date = str(from_date)
    to_date = str(to_date)
    from_date = from_date.split("-")[0] + from_date.split("-")[1] + from_date.split("-")[2]
    to_date = to_date.split("-")[0] + to_date.split("-")[1] + to_date.split("-")[2]

    if st.button("실행"):
        with st.spinner("wait.."):

            # 조달청 계약현황 URL
            url = "	http://apis.data.go.kr/1230000/CntrctInfoService/getCntrctInfoListThngPPSSrch"
            key = "kk21uIM463FsyxRw8huR6C%2FZreHho7dmXIdTe5j%2Feqa9XN6Dx%2F4Dh%2BxM%2FftZrpsS856Jicn3jtklnOac2TW9yQ%3D%3D"

            # 계약현황 기간 내 모든 페이지 가져오기
            i = 0
            total = []

            while True:
                i += 1
                queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode(
                    {
                        parse.quote_plus("inqryDiv"): "1",  # 필수
                        parse.quote_plus("pageNo"): i,  # 필수
                        parse.quote_plus("numOfRows"): "100",  # 필수
                        parse.quote_plus("prdctClsfcNoNm"): target_nm,  # 품명
                        parse.quote_plus("inqryBgnDate"): from_date,  # 조회시작일
                        parse.quote_plus("inqryEndDate"): to_date,  # 조회종료일
                        parse.quote_plus("type"): "json",
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

            st.write("총 " + str(len(total)) + "건을 찾았습니다.")

            # client 요청 형식
            lst_01 = []  # 계약번호
            lst_02 = []  # 공고명
            lst_03 = []  # 납기(일자)
            lst_04 = []  # 계약금액
            lst_05 = []  # 계약방법
            lst_06 = []  # 계약일자
            lst_07 = []  # 계약업체
            lst_empty = []  # 구분
            lst_08 = []  # 수요기관

            # 계약현황 json을 df로 추출
            for item in total:
                try:
                    """
                    <실제 컬럼명과 API명>
                    1. 계약번호: 확정계약번호(dcsnCntrctNo)
                    2. 공고명: 계약건명(cntrctNm)
                    3. 납기: 계약기간(cntrctPrd)
                    4. 계약금액: 금차계약금액(thtmCntrctAmt)
                    5. 계약방법: 계약체결방법명(cntrctCnclsMthdNm)
                    6. 계약일자: 계약체결일자(cntrctCnclsDate)
                    7. 계약업체: 업체목록(업체명) (corpList) --> 잘라와야 함
                    8. 구분
                    9. 수요기관: 수요기관명(cntrctInsttNm)
                    """

                    lst_01.append(item["dcsnCntrctNo"])
                    lst_02.append(item["cntrctNm"])
                    lst_03.append(item["cntrctPrd"])
                    lst_04.append(item["thtmCntrctAmt"])
                    lst_05.append(item["cntrctCnclsMthdNm"])
                    lst_06.append(item["cntrctCnclsDate"])
                    lst_07.append(item["corpList"])
                    lst_08.append(item["cntrctInsttNm"])
                except:
                    pass

            # 최종 df추출
            lst_empty_0 = [None] * len(lst_01)

            source = {
                "계약번호": lst_01,
                "공고명": lst_02,
                "납기": lst_03,
                "계약금액": lst_04,
                "계약방법": lst_05,
                "계약일자": lst_06,
                "계약업체": lst_07,
                "구분": lst_empty_0,
                "수요기관": lst_08,
            }
            df = pd.DataFrame(source)
            df["계약업체"] = df["계약업체"].str.split("^").str[3]
            AgGrid(df)

            # 엑셀로 추출
            try:
                df.to_excel('./naraContract.xlsx')
                st.write("(엑셀)추출 완료!")
            except Exception as e:
                st.write(e)

            with open("naraContract.xlsx", "rb") as file:
                btn = st.download_button(
                        label="Download Excel",
                        data=file,
                        file_name="naraContract.xlsx",
                        mime="application/vnd.ms-excel"
                )

            # # #MySQL과 연동
            # # conn = pymysql.connect(host='localhost', user='root', password='1562', db='file', charset='utf8')

            # # now = datetime.now()
            # # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

            # # try:
            # #     with conn.cursor() as curs:
            # #         sql = """INSERT INTO FILE VALUES (%s, %s, %s, %s, %s, %s)"""
            # #         curs.execute(sql, ('naraContract.xlsx', 'naraContract.xlsx', 0, formatted_date, 'excel', '100KB'))
            # #     conn.commit()
            # # except Exception as e:
            # #     print(e)
            # # finally:
            # #     conn.close()



