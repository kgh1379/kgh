import streamlit as st 
from docx import Document
from docx2pdf import convert
from datetime import datetime
import pythoncom
from pymongo import MongoClient
import pandas as pd

pythoncom.CoInitialize()

# MongoDB에 연결
client = MongoClient('localhost', 27017)
db = client['education']
collection =  db['results']

st.title("수료증 발급 서비스")

name = st.text_input("이름을 입력하세요")
course = st.selectbox("과정 선택", ["파이썬 입문 과정", "웹해킹분석", "포렌식분석"])
date = st.text_input("날짜를 선택하세요. ex) 2023년 12월 1일")

if st.button("수료증 생성"):
    # 수료증 발급 DB 저장
    result_data = {
        'name': name,
        'course': course,
        'date': date,
        'timestamp': datetime.now()
    }
    collection.insert_one(result_data)
    
    doc = Document('templates.docx')
    
    for paragraph in doc.paragraphs:
        if 'NAME' in paragraph.text:
            paragraph.text = paragraph.text.replace('NAME',name)
        elif 'COURSE' in paragraph.text:
            paragraph.text = paragraph.text.replace('COURSE',course)
        elif 'DATE' in paragraph.text:
            paragraph.text = paragraph.text.replace('DATE',date)
            
    doc_file = f'{name}_{course}_수료증.docx'
    pdf_file = f'{name}_{course}_수료증.pdf'
    doc.save(doc_file)
    convert(doc_file, pdf_file)
    
    st.success("수료증 생성이 완료되었습니다. 아래버튼으로 다운받으세요")
    
    with open(pdf_file, 'rb') as f:
        pdf_bytes = f.read()
    st.download_button(label="수료증 다운로드", data=pdf_bytes, file_name=pdf_file)
    
    st.title("발급 목록")
    data_from_mongodb = collection.find()
    df=pd.DataFrame(data_from_mongodb, columns=['name', 'course', date])
    st.dataframe(df)