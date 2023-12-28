import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, time, timedelta

# Function to create and get the database connection
@st.cache_resource
def get_connection():
    conn = sqlite3.connect('tc99m_activity_data.db', check_same_thread=False)
    return conn

# Initialize connection
conn = get_connection()

# Function to create table if it doesn't exist
def create_table():
    conn.execute("DROP TABLE IF EXISTS tc99m_activity")  # Drop the existing table
    conn.execute("""
        CREATE TABLE tc99m_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calibration_date DATE,
            calibration_time TIME,
            delivery_date DATE,
            elution_date DATE,
            elution_time TIME,
            initial_activity_mo99 REAL,
            activity_mci REAL,
            year INTEGER,
            month INTEGER,
            weekday INTEGER,
            day INTEGER,
            
        )
    """)
    conn.commit()
    
def get_statistics(time_frame, time_value):
    # For 'Week', the time_value will be the start weekday
    if time_frame == "week":
        start_weekday = time_value
        end_weekday = 4  # Friday
        query = """
            SELECT elution_date, SUM(activity_mci) as total_activity
            FROM tc99m_activity
            WHERE weekday >= ? AND weekday <= ?
            GROUP BY elution_date
            ORDER BY elution_date DESC
            LIMIT 5
        """
        params = (start_weekday, end_weekday)
    else:
        # For 'Year', 'Month', and 'Day'
        query = f"""
            SELECT elution_date, SUM(activity_mci) as total_activity
            FROM tc99m_activity
            WHERE {time_frame} = ?
            GROUP BY elution_date
            ORDER BY elution_date DESC
            LIMIT 5
        """

# Streamlit UI for Statistics
st.sidebar.title("Mo-Generator")
view_mode = st.sidebar.selectbox("Choose View Mode", ["Calculator", "Statistics"])

if view_mode == "Statistics":
    st.title("Recorded Data Statistics")
    time_frame = st.selectbox("Select Time Frame", ["Year", "Month", "Day", "Week"])
    if time_frame == "Year":
        selected_year = st.selectbox("Select Year", list(range(2020, datetime.now().year + 1)))
        statistics_data = get_statistics('year', selected_year)
    elif time_frame == "Month":
        selected_month = st.selectbox("Select Month", list(range(1, 13)))
        statistics_data = get_statistics('month', selected_month)
    elif time_frame == "Day":
        selected_day = st.selectbox("Select Day", list(range(1, 32)))
        statistics_data = get_statistics('day', selected_day)
    elif time_frame == "Week":
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        selected_weekday = st.selectbox("Select Start Day", weekdays, index=weekdays.index("Monday"))
        weekday_number = weekdays.index(selected_weekday)
        statistics_data = get_statistics(weekday_number)
    
    st.write("Recent Entries and Sum of Activity")
    st.table(statistics_data)

# Function to add data to the database
def add_data(calibration_date, calibration_time, delivery_date, elution_date, elution_time, initial_activity_mo99, activity_mci):
    # elution_date is already a datetime.date object, so directly extract year, month, and day
    year, month, day = elution_date.year, elution_date.month, elution_date.day
    weekday = elution_date.weekday()

    # Check if calibration_time and elution_time are datetime.time objects
    if isinstance(calibration_time, time):
        calibration_time = calibration_time.strftime('%H:%M')
    if isinstance(elution_time, time):
        elution_time = elution_time.strftime('%H:%M')

    conn.execute("""
        INSERT INTO tc99m_activity 
        (calibration_date, calibration_time, delivery_date, elution_date, elution_time, initial_activity_mo99, activity_mci, year, month, day, weekday)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (calibration_date, calibration_time, delivery_date, elution_date, elution_time, initial_activity_mo99, activity_mci, year, month, day, weekday))
    conn.commit()

# Function to calculate Tc-99m activity
def calculate_tc99m_activity(initial_activity_mo99, half_life_mo99, half_life_tc99m, elapsed_time_mo99, elapsed_time_tc99m):
    current_activity_mo99 = initial_activity_mo99 * (0.5 ** (elapsed_time_mo99 / half_life_mo99))
    actual_activity_tc99m = current_activity_mo99 * (0.5 ** (elapsed_time_tc99m / half_life_tc99m))
    return actual_activity_tc99m

# Streamlit UI
st.title('Tc-99m Activity Calculator')

# User inputs
calibration_date = st.date_input('Calibration Date')
calibration_time = st.time_input('Calibration Time', value=datetime.strptime('09:00', '%H:%M').time())
delivery_date = st.date_input('Delivery Date')
elution_date = st.date_input('Elution Date')
elution_time = st.time_input('Elution Time', value=datetime.strptime('08:00', '%H:%M').time())
initial_activity_mo99 = st.number_input('Initial Mo-99 Activity (GBq)', value=55.5)

# Mo-99 half-life and initial activity
half_life_mo99 = 66  # hours
half_life_tc99m = 6  # hours


# Calculate activity
if st.button('Calculate Activity'):
    # Calculate elapsed time for Mo-99 and Tc-99m
    calibration_datetime = datetime.combine(calibration_date, calibration_time)
    delivery_datetime = datetime.combine(delivery_date, calibration_time)
    elution_datetime = datetime.combine(elution_date, elution_time)
    elapsed_time_mo99 = (delivery_datetime - calibration_datetime).total_seconds() / 3600
    elapsed_time_tc99m = (elution_datetime - delivery_datetime).total_seconds() / 3600

    # Calculate Tc-99m activity
    activity_tc99m_gbq = calculate_tc99m_activity(initial_activity_mo99, half_life_mo99, half_life_tc99m, elapsed_time_mo99, elapsed_time_tc99m)
    activity_tc99m_mci = activity_tc99m_gbq * 27000  # Convert GBq to mCi
# Save data to database
    add_data(calibration_date, calibration_time.strftime('%H:%M'), delivery_date, elution_date, elution_time.strftime('%H:%M'), initial_activity_mo99, activity_tc99m_mci)

    # Show success message
    st.success('Data saved successfully!')

    # Display calculated activity in mCi
    st.write(f"Calculated Tc-99m Activity at {elution_time.strftime('%H:%M')}: {activity_tc99m_mci:.2f} mCi")

    # Create a DataFrame for displaying results
    result_df = pd.DataFrame({
        'Date': [elution_date],
        'Time': [elution_time.strftime('%H:%M')],
        'Tc-99m Activity (mCi)': [round(activity_tc99m_mci, 2)]
    })

    # Display the table
    st.table(result_df)

# Create the table in the database
create_table()
# Run the app with the command: streamlit run your_script_name.py