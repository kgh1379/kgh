import streamlit as st
import pandas as pd
from utils import database  # 데이터베이스 연동을 위한 유틸리티 모듈 임포트

def storage_page():
    st.title("Storage Status")

    # 데이터베이스에서 보관 항목 데이터 가져오기
    storage_items = database.get_storage_items()  # database.py에 해당 함수 구현 필요

    # 데이터프레임으로 변환
    df_storage = pd.DataFrame(storage_items, columns=['ID', 'Acquisition Date', 'Lot/Batch No', 'Expected Dispatch Date', 'Checker'])

    # 스트림릿을 사용하여 테이블로 표시
    st.write("### Storage Items")
    st.dataframe(df_storage)

    # 출고예정일이 1개월 이내인 항목에 대해 알림 기능 구현
    # 알림 발송 로직은 'notifications.py'에 구현
