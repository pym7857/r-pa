import streamlit as st
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import requests
import pandas as pd
from urllib import parse
from st_aggrid import AgGrid

def dart():

    sidebar = st.sidebar
    sidebar.header("Settings")


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
    YEAR = sidebar.text_input('연도', '2019')
    CODE = sidebar.selectbox('기간', ('1분기보고서', '반기보고서', '3분기보고서', '사업보고서'))
    CORP_NAME = sidebar.text_input('회사이름', '효성중공업').replace(" ", "").strip()

    CODE_DICT = {'1분기보고서': '11013', '반기보고서' : '11012', '3분기보고서' : '11014', '사업보고서' : '11011'}
    CODE = CODE_DICT[CODE]

    if st.button("실행"):
        with st.spinner("wait.."):

            try:
                corp_code = find_corp_num(CORP_NAME)
                print(corp_code)
            except Exception as e:
                print(e)
                print('해당 회사 명이 없습니다.')


            #https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml?crtfc_key=5f1d10ac04bc83ed14b340b5a39a0418bd0261c6&corp_code=01205851&bsns_year=2019&reprt_code=11014&fs_div=CFS
            #단일회사 전체 재무제표 API
            url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.xml' # xml로 가져옵니다.

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

            st.write(len(root))

            classification_list = []
            try:
                for i in root.iter('sj_nm'): # 재무제표 명
                    classification_list.append(i.text)
            except:
                classification_list = [None]*len(len(root))

            accnt_list = []
            try:
                for i in root.iter('account_nm'): # 계정명
                    accnt_list.append(i.text)
            except:
                accnt_list = [None]*len(len(root))

            price_list = []
            try:
                for i in root.iter('thstrm_amount'): # 당기금액
                    if (type(i.text) == str):
                        price_list.append(format(int(i.text), ","))
                    else:
                        price_list.append(i.text)
            except:
                price_list = [None]*len(len(root))

            period_list = []
            try:
                for i in root.iter('thstrm_nm'): # 당기명
                    period_list.append(i.text)
            except:
                period_list = [None]*len(len(root))


            source = { # columns
                '재무제표명': classification_list,
                '당기명': period_list,
                CORP_NAME: price_list,
            }
            df = pd.DataFrame(source, index=accnt_list)
            AgGrid(df)
            #print(df.loc['유동자산'][CORP_NAME]) # 가격이 나옴

            try:
                df.to_excel('./dart.xlsx')
                st.write('(python)추출 완료!')
            except Exception as e:
                print(e)
                st.write('(python)추출 에러!')

            with open("dart.xlsx", "rb") as file:
                btn = st.download_button(
                        key="dart.xlsx,",
                        label="Download Excel",
                        data=file,
                        file_name="dart.xlsx",
                        mime="application/vnd.ms-excel"
                )
