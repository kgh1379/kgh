import json
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
#with open(r'C:\Users\kjh4253\Documents\GitHub\kgh\SalaryCalculate\salary_info.json', 'r') as file:
    #employee_info = json.load(file)

# 데이터 로드 함수
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"{file_path} 파일을 찾을 수 없습니다.")
        return None

# 직원 데이터 및 급여 정보 로드
employee_data = load_json_data(fr'C:\Users\kjh4253\Documents\GitHub\kgh\SalaryCalculate\{employee_id}.json')
salary_info = load_json_data(r'C:\Users\kjh4253\Documents\GitHub\kgh\SalaryCalculate\salary_info.json')

# 데이터 로드 및 유효성 검증
employee_data = load_json_data(f'{employee_id}.json')
if not employee_data:
    st.stop()

salary_info = load_json_data('salary_info.json')
if not salary_info:
    st.stop()

# 근무 연수 계산 함수
def calculate_years_of_service(joining_date_str, current_date):
    joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d")
    total_years = current_date.year - joining_date.year
    if (current_date.month, current_date.day) < (joining_date.month, joining_date.day):
        total_years -= 1
    return total_years

# 승진 로직 함수
def calculate_promotion_date(employee_data):
    leave_start = datetime.strptime(employee_data["leaveOfAbsence"]["start"], "%Y-%m-%d")
    leave_end = datetime.strptime(employee_data["leaveOfAbsence"]["end"], "%Y-%m-%d")
    current_start_year = datetime.strptime(employee_data["salaryClass"]["current"]["startYear"], "%Y-%m-%d")
    years_in_class = employee_data["salaryClass"]["current"]["yearsInClass"]

    unpaid_leave_duration = leave_end - leave_start
    promotion_delay = unpaid_leave_duration.days // 365

    promotion_date = current_start_year.replace(year=current_start_year.year + years_in_class + promotion_delay)
    if promotion_date.day != 1:
        promotion_date = promotion_date.replace(day=1) + timedelta(days=31)
        promotion_date = promotion_date.replace(day=1)

    next_class = "S1"
    next_years_in_class = 1

    return {
        "promotionDate": promotion_date.strftime("%Y-%m-%d"),
        "nextClass": next_class,
        "nextYearsInClass": next_years_in_class
    }

# 근무 연수 및 승진 정보 계산
years_of_service = calculate_years_of_service(employee_data["yearsOfJoining"], current_date)
promotion_info = calculate_promotion_date(employee_data)

# 급여 클래스 및 근무 연수에 따른 급여 정보 추출
salary_class = employee_data["salaryClass"]["current"]["class"]
years_in_class = str(employee_data["salaryClass"]["current"]["yearsInClass"])
salary_details = employee_data["salaryClassDetails"][salary_class][years_in_class]

# 가계 지원 수당을 지급하는 월 설정
household_allowance_months = [3, 4, 5, 6, 7, 8, 10, 11, 12]
household_allowance_months.extend(holiday_months)
holiday_allowance_months = [5, 7]
holiday_allowance_months.extend(holiday_months) 

# 입력사항
holiday_workdays = st.number_input('휴일 근무일', min_value=0)
family_care_leave_days = st.number_input('가족 돌봄 휴가일', min_value=0)
annual_leave_days = st.number_input('연차 휴가일', min_value=0)

# 근무 연수 계산
years_of_service = calculate_years_of_service(employee_data["yearsOfJoining"], current_date)
# Determine tenure addition salary rate based on years of service
if years_of_service <= 5:
    tenure_addition_salary_rate = employee_data["tenureAdditionSalaryRate"]["1_to_5_years"]
elif 5 < years_of_service <= 10:
    tenure_addition_salary_rate = employee_data["tenureAdditionSalaryRate"]["5_to_10_years"]
elif 10 < years_of_service <= 15:
    tenure_addition_salary_rate = employee_data["tenureAdditionSalaryRate"]["10_to_15_years"]
elif 15 < years_of_service <= 20:
    tenure_addition_salary_rate = employee_data["tenureAdditionSalaryRate"]["15_to_20_years"]
else:
    tenure_addition_salary_rate = employee_data["tenureAdditionSalaryRate"]["20_plus_years"]

# 장기근속 수당 계산
long_term_service_allowance = 0
if 5 <= years_of_service <= 10:
    long_term_service_allowance = employee_data["longTermServiceAllowance"]["5_to_10_years"]
elif 10 < years_of_service <= 15:
    long_term_service_allowance = employee_data["longTermServiceAllowance"]["10_to_15_years"]
elif 15 < years_of_service <= 20:
    long_term_service_allowance = employee_data["longTermServiceAllowance"]["15_to_20_years"]
elif years_of_service > 20:
    long_term_service_allowance = 100000  # 20년 초과 기본 수당
    if years_of_service > 21:
        long_term_service_allowance += (years_of_service - 20) * 10000  # 21년 이상 추가 가산금
    if years_of_service > 25:
        long_term_service_allowance += (years_of_service - 25) * 30000  # 25년 이상 추가 가산금


# 기본 급여, 역량 급여, 보너스, 가계 지원 수당 추출
standard_basic_salary = salary_details
competency_pay = employee_data["salaryClassDetails"][salary_class]["competencyPay"]
bonus = employee_data["salaryClassDetails"][salary_class]["bonus"]

# 조정 급여, 식사 지원 수당, 교통 지원 수당 추출 등 
adjustment_pay = employee_data["adjustmentPay"]
meal_assistance_allowance = employee_data["mealAssistanceAllowance"]
transportation_assistance_allowance = employee_data["transportationAssistanceAllowance"]
tenure_addition_salary = round((standard_basic_salary + (adjustment_pay / 2)) * tenure_addition_salary_rate)
basic_salary = standard_basic_salary + tenure_addition_salary
holiday_support_allowance = (basic_salary + (adjustment_pay / 2)) * 0.5


# 명절 지원 수당 초기화
holiday_support_allowance = 0
if current_month in holiday_allowance_months:
    holiday_support_allowance = (basic_salary + (adjustment_pay / 2)) * 0.5

household_support_allowance = 0
if current_month in household_allowance_months:
    household_support_allowance = employee_data["salaryClassDetails"][salary_class]["householdSupportAllowance"]


# 총 급여 계산
total_salary = standard_basic_salary + competency_pay + bonus + household_support_allowance + \
               adjustment_pay + meal_assistance_allowance + transportation_assistance_allowance + \
               tenure_addition_salary + long_term_service_allowance + holiday_support_allowance

# 본문
if st.button('계산하기'):
    st.table([
        ("항목", "금액", "비고"),
        (f"승진 예정일: {promotion_info['promotionDate']}"),
        (f"다음 Salary Class: {promotion_info['nextClass']} {promotion_info['nextYearsInClass']}년차"),
        (f"기본기준급 ({salary_class}, {years_in_class}년차)","{:,}".format(standard_basic_salary)),
        (f"근속가산기본급 ({round(tenure_addition_salary_rate*100)}%)", "{:,}".format(tenure_addition_salary)),
        (f"장기근속수당 ({years_of_service})", "{:,}".format(long_term_service_allowance)),
        ("능력금", "{:,}".format(competency_pay)),
        ("상여금", "{:,}".format(bonus)),
        ("가계지원비", "{:,}".format(household_support_allowance)),
        ("조정급여", "{:,}".format(adjustment_pay)),
        ("식사 지원 수당", "{:,}".format(meal_assistance_allowance)),
        ("교통 지원 수당", "{:,}".format(transportation_assistance_allowance)),
        ("명절 지원 수당", "{:,}".format(holiday_support_allowance)),
        ("총 급여", "{:,}".format(total_salary)),
    ])


