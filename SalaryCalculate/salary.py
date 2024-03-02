import json
import streamlit as st
from datetime import datetime, timedelta

# Load JSON data
with open(r'C:\Users\kjh4253\Documents\GitHub\kgh\SalaryCalculate\salary_info.json', 'r') as file:
    employee_info = json.load(file)

# Calculate years of service
def calculate_years_of_service(joining_date_str, current_date):
    joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d")
    total_years = current_date.year - joining_date.year
    if (current_date.month, current_date.day) < (joining_date.month, joining_date.day):
        total_years -= 1
    return total_years

# Streamlit UI
st.title('급여 계산기')
year = st.number_input("연도", min_value=2000, max_value=2030, value=2024)
month = st.number_input("월", min_value=1, max_value=12, value=2)
current_date = datetime(year, month, 1)

holiday_workdays = st.number_input('휴일 근무일', min_value=0)
family_care_leave_days = st.number_input('가족 돌봄 휴가일', min_value=0)
annual_leave_days = st.number_input('연차 휴가일', min_value=0)

# 근무 연수 계산
years_of_service = calculate_years_of_service(employee_info["yearsOfJoining"], current_date)
# joining_date = datetime.strptime(employee_info["yearsOfJoining"], "%Y-%m-%d")

# 급여 클래스 및 근무 연수에 따른 급여 정보 추출
salary_class = employee_info["salaryClass"]["current"]["class"]
years_in_class = str(employee_info["salaryClass"]["current"]["yearsInClass"])
salary_details = employee_info["salaryClassDetails"][salary_class][years_in_class]

# 기본 급여, 역량 급여, 보너스, 가계 지원 수당 접근
standard_basic_salary = salary_details
adjustment_pay = employee_info["adjustmentPay"]
competency_pay = employee_info["salaryClassDetails"][employee_info["salaryClass"]]["competencyPay"]
bonus = employee_info["salaryClassDetails"][employee_info["salaryClass"]]["bonus"]

holiday_workdays = st.number_input('휴일 근무일', min_value=0)
family_care_leave_days = st.number_input('가족 돌봄 휴가일', min_value=0)
annual_leave_days = st.number_input('연차 휴가일', min_value=0)

household_support_allowance = employee_info["salaryClassDetails"][employee_info["salaryClass"]]["householdSupportAllowance"]
tenure_addition_salary = (standard_basic_salary + (adjustment_pay / 2)) * (employee_info["salaryClassDetails"]["tenureAdditionSalaryRate"])
long_term_service_allowance = employee_info["salaryClassDetails"][employee_info["salaryClass"]]["longTermServiceAllowance"]
basic_salary = standard_basic_salary + tenure_addition_salary
holiday_support_allowance = (basic_salary + adjustment_pay / 2) * 0.5
meal_assistance_allowance = employee_info["mealAssistanceAllowance"]
transportation_assistance_allowance = employee_info["transportationAssistanceAllowance"]

if st.button('계산하기'):
    # Total Salary Calculation
    total_salary = standard_basic_salary + competency_pay + bonus + household_support_allowance + \
               adjustment_pay + meal_assistance_allowance + transportation_assistance_allowance
