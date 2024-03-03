import json
import sqlite3
import streamlit as st
from datetime import datetime, timedelta
import requests
from xml.etree import ElementTree

# Streamlit UI 구성
st.title("급여 계산기")
# 사이드바 설정
st.sidebar.title("직원 정보")
employee_id = st.sidebar.text_input("사번을 입력하세요:", value="20842")
# 본문
year = st.number_input("연도", min_value=2000, max_value=2030, value=2024)
month = st.number_input("월", min_value=1, max_value=12, value=2)
current_date = datetime(year, month, 1)
current_month = current_date.month
current_year = current_date.year
current_month_str = f"{current_date.month:02d}"  # 월 정보를 두 자리 문자열로 포맷팅 (예: 2월 -> '02')

# OpenAPI 인증키 (URL 인코딩된 상태)
service_key = "rdRLE%2FHyy67UTtFIWVweDWoayloqCbA5a%2FFrXMSKhdFefs%2FSkgl8VbtJMQsnzZhjkFWBEN6K4f%2FqqStu6Rhhig%3D%3D"
# OpenAPI 요청 URL
url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getHoliDeInfo"

# API 요청 파라미터 설정
params = {
    'serviceKey': service_key,
    'pageNo': '1',
    'numOfRows': '10',
    'solYear': str(current_year),
    'solMonth': current_month_str
}
# API 요청 및 응답 (가정)
response = requests.get(url, params=params)
# 응답으로부터 설날과 추석이 있는 달 확인 (가정)

# 응답 XML 파싱 (가정)
root = ElementTree.fromstring(response.content)
holiday_months = []

for item in root.findall('.//item'):
    itemNameElement = item.find('dateName')
    if itemNameElement is not None:  # itemNameElement가 None이 아닐 때만 .text에 접근
        itemName = itemNameElement.text
        if itemName in ['설날', '추석']:
            eventDate = item.find('locdate').text  # 'YYYYMMDD' 형식
            eventMonth = int(eventDate[4:6])  # 월 정보 추출
            if eventMonth not in holiday_months:
                holiday_months.append(eventMonth)

# JSON 데이터 로드
#with open(r'C:/Users/kjh4253/Documents/GitHub/kgh/SalaryCalculate/salary_info.json', 'r') as file:
    #employee_info = json.load(file)

conn = sqlite3.connect('C:/Users/kjh4253/Documents/GitHub/kgh/SalaryCalculate/{employee_id}.db')
conn = sqlite3.connect('C:/Users/kjh4253/Documents/GitHub/kgh/SalaryCalculate/salary_info.db')
c = conn.cursor()

# 직원 정보 로드 함수
def load_employee_data(employee_id):
    c.execute("SELECT * FROM employee WHERE employeeId = ?", (employee_id,))
    return c.fetchone()

# 급여 정보 로드 함수
def load_salary_info():
    c.execute("SELECT * FROM salary_info")
    return c.fetchall()

# 직원 정보 로드
employee_data = load_employee_data(employee_id)

# 급여 정보 로드
salary_info = load_salary_info()

print(employee_data)
print(salary_info)