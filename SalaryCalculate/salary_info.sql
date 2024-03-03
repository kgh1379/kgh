-- Create a table for salary class details
CREATE TABLE salary_class_details (
    class TEXT PRIMARY KEY,
    tier INTEGER,
    salary INTEGER,
    competency_pay INTEGER,
    bonus INTEGER,
    household_support_allowance INTEGER
);

-- Insert data into the salary_class_details table
INSERT INTO salary_class_details (class, yearsInClass, salary, competency_pay, bonus, household_support_allowance) VALUES 
('M1', 1, 3632400, 1625200, 204000, 1217043),
('M1', 2, 3663000, 1625200, 204000, 1217043),
('M1', 3, 3693500, 1625200, 204000, 1217043),
('M1', 4, 3724000, 1625200, 204000, 1217043),
('M1', 5, 3755300, 1625200, 204000, 1217043),
('M1', 6, 3786600, 1625200, 204000, 1217043),
('M1', 7, 3818800, 1625200, 204000, 1217043),
('M1', 8, 3851100, 1625200, 204000, 1217043),
('S3', 1, 3364000, 1350700, 197200, 1175725),
('S3', 2, 3396900, 1350700, 197200, 1175725),
('S3', 3, 3429900, 1350700, 197200, 1175725),
('S3', 4, 3463900, 1350700, 197200, 1175725),
('S3', 5, 3498100, 1350700, 197200, 1175725),
('S3', 6, 3532000, 1350700, 197200, 1175725),
('S3', 7, 3566700, 1350700, 197200, 1175725),
('S3', 8, 3601500, 1350700, 197200, 1175725),
('S2', 1, 3063800, 1213200, 177300, 1055526),
('S2', 2, 3094200, 1213200, 177300, 1055526),
('S2', 3, 3124900, 1213200, 177300, 1055526),
('S2', 4, 3155300, 1213200, 177300, 1055526),
('S2', 5, 3187300, 1213200, 177300, 1055526),
('S2', 6, 3218600, 1213200, 177300, 1055526),
('S2', 7, 3250633, 1213200, 177300, 1055526),
('S2', 8, 3282000, 1213200, 177300, 1055526),
('S1', 1, 2766900, 1075700, 157400, 934971),
('S1', 2, 2794100, 1075700, 157400, 934971),
('S1', 3, 2821867, 1075700, 157400, 934971),
('S1', 4, 2850100, 1075700, 157400, 934971),
('S1', 5, 2878600, 1075700, 157400, 934971),
('S1', 6, 2906500, 1075700, 157400, 934971),
('S1', 7, 2935400, 1075700, 157400, 934971),
('S1', 8, 2964200, 1075700, 157400, 934971),
('J3', 1, 2463800, 747100, 156700, 930678),
('J3', 2, 2488300, 747100, 156700, 930678),
('J3', 3, 2513100, 747100, 156700, 930678),
('J3', 4, 2537800, 747100, 156700, 930678),
('J3', 5, 2562900, 747100, 156700, 930678),
('J3', 6, 2587700, 747100, 156700, 930678),
('J3', 7, 2613800, 747100, 156700, 930678),
('J3', 8, 2638800, 747100, 156700, 930678);

-- Create a table for tenure addition salary rate
CREATE TABLE tenure_addition_salary_rate (
    tenure_range TEXT PRIMARY KEY,
    rate REAL
);

-- Insert data into the tenure_addition_salary_rate table
INSERT INTO tenure_addition_salary_rate (tenure_range, rate) VALUES 
('1_to_5_years', 0.02),
('5_to_10_years', 0.05),
('10_to_15_years', 0.06),
('15_to_20_years', 0.07),
('20_plus_years', 0.08);

-- Create a table for long term service allowance
CREATE TABLE long_term_service_allowance (
    tenure_range TEXT PRIMARY KEY,
    allowance INTEGER
);

-- Insert data into the long_term_service_allowance table
INSERT INTO long_term_service_allowance (tenure_range, allowance) VALUES 
('5_to_10_years', 50000),
('10_to_15_years', 60000),
('15_to_20_years', 80000),
('20_to_25_years', 100000),
('additional_21_years', 10000),
('additional_25_years', 30000);

-- Create a table for severance allowance payment rate
CREATE TABLE severance_allowance_payment_rate (
    tenure_range TEXT PRIMARY KEY,
    rate REAL
);

-- Insert data into the severance_allowance_payment_rate table
INSERT INTO severance_allowance_payment_rate (tenure_range, rate) VALUES 
('1_to_5_years', 0.1),
('5_to_10_years', 0.35),
('10_to_15_years', 0.45),
('15_to_20_years', 0.5),
('20_plus_years', 0.6);

-- Create a table for severance pay payment rate
CREATE TABLE severance_pay_payment_rate (
    years_of_service INTEGER PRIMARY KEY,
    rate REAL
);
