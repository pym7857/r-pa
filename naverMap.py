import streamlit as st
import xml.etree.ElementTree as ET
import requests
import pymysql
from datetime import datetime
import json
import requests
import pandas as pd
from urllib import parse
import sys
from st_aggrid import AgGrid

def naverMap():
    for i in range(2021,2031):
        with open(f"./data/naverMap/naverMap({i}년 검색결과).xlsx", "rb") as file:
            btn = st.download_button(
                    key=f"naverMap({i}년 검색결과).xlsx,",
                    label=f"naverMap({i}년 검색결과).xlsx",
                    data=file,
                    file_name=f"naverMap({i}년 검색결과).xlsx",
                    mime="application/vnd.ms-excel"
            )