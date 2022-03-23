import streamlit as st

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
