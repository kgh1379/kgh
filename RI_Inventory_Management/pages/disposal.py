import streamlit as st
import pandas as pd
from utils import database  # 데이터베이스 연동을 위한 유틸리티 모듈 임포트

def disposal_page():
    st.title("Disposal Status")

    # 데이터베이스에서 폐기
