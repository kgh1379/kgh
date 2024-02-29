// The salary calculation logic will be added here
function calculateSalary() {
    // Assuming salaryData is loaded via a script tag or fetched from a server
    // Also assuming that salaryData contains all the necessary constants and salary tables
    const salaryData = {}; // Replace with actual data

    // Get the selected month from the dropdown
    const monthSelect = document.getElementById('month-select');
    const selectedMonth = monthSelect.value;

    // Perform salary calculation based on the selected month
    const basicSalary = salaryData.salaryClassDetails.J3.basicSalary;
    const adjustmentPay = salaryData.adjustmentPay;
    const tenureAddition = (basicSalary + (adjustmentPay / 2)) * salaryData.tenureAdditionRate['15_to_20_years'];
    const longTermServiceAllowance = salaryData.longTermServiceAllowance['15_to_20_years'];
    let holidaySupportAllowance = 0;
    if (salaryData.holidaySupportAllowanceMonths.includes(parseInt(selectedMonth))) {
        holidaySupportAllowance = (basicSalary + (adjustmentPay / 2)) * 0.5;
    }
    let householdSupportAllowance = salaryData.salaryClassDetails.J3.householdSupportAllowance;
    if (!salaryData.householdSupportAllowanceMonths.includes(parseInt(selectedMonth))) {
        householdSupportAllowance = 0;
    }
    

    // Calculate total salary
    const totalSalary = basicSalary + tenureAddition + longTermServiceAllowance + holidaySupportAllowance +
                        competencyPay + bonus + householdSupportAllowance + mealAssistance + transportationAssistance;

    // Display the salary in the salary-display section
    const salaryDisplaySection = document.getElementById('salary-display');
    salaryDisplaySection.textContent = '총 급여: ' + totalSalary.toLocaleString() + '원';
}

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