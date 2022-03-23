import streamlit as st

from contract import *
from exchange import *
from bid import *
from dart import *
from naverMap import *


def app():
    sidebar = st.sidebar
    sidebar.header("Settings")

    pages = {
        "계약현황": contract,
        "입찰공고": bid,
        "환율": exchange,
        "DART": dart,
        "네이버 지도(연도별)" : naverMap
    }

    st.sidebar.title("r-pa")

    # Radio buttons to select desired option
    page = st.sidebar.radio("", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page]()

if __name__ == "__main__":
    app()