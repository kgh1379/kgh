// 가정: `salaryData`는 JSON 파일로부터 불러온 급여 데이터입니다.
const salaryData = {/* JSON 데이터 삽입 */};

function calculateSalary(date, employeeDetails) {
    const salaryData = {}; // Replace with actual data
    // 날짜 객체 생성 및 현재 월 가져오기
    // const currentDate = new Date(date);
    // const currentMonth = currentDate.getMonth() + 1; // JavaScript에서 월은 0부터 시작하므로 1을 더해줌
    // Get the selected month from the dropdown
    const monthSelect = document.getElementById('month-select');
    const selectedMonth = monthSelect.value;

    // 직급과 연차 정보를 JSON 데이터에서 추출
    const { salaryClass, yearsOfEmployment } = employeeDetails;
    // const salaryClass = salaryData.salaryClass.current.class; // 현재 직급
    // const yearsOfEmployment = salaryData.salaryClass.current.yearsInClass; // 해당 직급에서의 연수
    const classData = salaryData.salaryClassTable[salaryClass];
    const tenureRate = getTenureAdditionSalaryRate(yearsOfEmployment);

    // 기본 급여 계산
    // Perform salary calculation based on the selected month
    const standardBasicSalary = classData[yearsOfEmployment.toString()];
    const adjustmentPay = salaryData.adjustmentPay;
    const tenureAdditionSalary = (standardBasicSalary + (adjustmentPay / 2)) * tenureRate;
    const basicSalary = standardBasicSalary + tenureAdditionSalary;
    const longTermServiceAllowance = getLongTermServiceAllowance(yearsOfEmployment);
    const competencyPay = salaryData.salaryClassDetails.J3.competencyPay;
    const bonus = salaryData.salaryClassDetails.J3.bonus;
    const mealAssistanceAllowance = salaryData.mealAssistanceAllowance;
    const transportationAssistanceAllowance = salaryData.transportationAssistanceAllowance;

    // 각종 수당 계산
    let holidaySupportAllowance = 0;
    if (salaryData.holidaySupportAllowanceMonths.includes(parseInt(selectedMonth))) {
        holidaySupportAllowance = (basicSalary + (adjustmentPay / 2)) * 0.5;
    }
    let householdSupportAllowance = salaryData.salaryClassDetails.J3.householdSupportAllowance;
    if (!salaryData.householdSupportAllowanceMonths.includes(parseInt(selectedMonth))) {
        householdSupportAllowance = 0;
    }
        

    // 연차 수당 계산 (가정: 연차 일수에 대한 정보가 필요합니다)
    const annualLeaveAllowance = calculateAnnualLeaveAllowance(employeeDetails.annualLeaveDays, basicSalary, householdSupportAllowance, holidaySupportAllowance);

    // 정규 임금 계산
    const ordinaryWage = standardBasicSalary + tenureAdditionSalary + longTermServiceAllowance + classData.competencyPay + classData.bonus + adjustmentPay;

    // 초과 근무, 휴일 근무 및 야간 근무 수당 계산 (가정: 각 근무 시간에 대한 정보가 필요합니다)
    const overtimeWorkAllowance = calculateOvertimeWorkAllowance(employeeDetails.overtimeHours, ordinaryWage);
    const holidayWorkAllowance = calculateHolidayWorkAllowance(employeeDetails.holidayHours, ordinaryWage);
    const nightWorkAllowance = calculateNightWorkAllowance(employeeDetails.nightHours, ordinaryWage);

    // 총 급여 계산
    const totalSalary = basicSalary + tenureAddition + longTermServiceAllowance + holidaySupportAllowance +
    competencyPay + bonus + householdSupportAllowance + mealAssistance + transportationAssistance;
    
    // 급여 표시 업데이트
    const salaryDisplaySection = document.getElementById('salary-display');
    salaryDisplaySection.textContent = '총 급여: ' + totalSalary.toLocaleString() + '원';
    
    return totalSalary;
}


function isHolidayMonth(currentMonth) {
    // 명절 지원비가 지급되는 달: 설날(1월 또는 2월), 추석(8월 또는 9월), 5월, 7월
    const holidayMonths = [1, 2, 5, 7, 8, 9]; // 실제 명절이 있는 월에 맞게 조정 필요
    return holidayMonths.includes(currentMonth);
  }
  
  function isHouseholdSupportMonth(currentMonth) {
    // 가계 지원비가 지급되지 않는 달: 1월, 9월 (예시, 실제 비지급 월에 따라 조정 필요)
    const nonPaymentMonths = [1, 9]; 
    return !nonPaymentMonths.includes(currentMonth);
  }
  
  // 날짜 예시: '2024-03-17'
  console.log(calculateSalary('2024-03-17', employeeDetails));
  
  // Populate month select options
function populateMonthSelect() {
    const monthSelect = document.getElementById('month-select');
    for (let i = 1; i <= 12; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i + '월';
        monthSelect.appendChild(option);
    }
}

document.addEventListener('DOMContentLoaded', populateMonthSelect);