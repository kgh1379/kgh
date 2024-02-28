import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dashboard_page():
    st.title("Dashboard")

    # Date Range Picker for Filtering
    start_date, end_date = st.select_slider(
        "Select Date Range:",
        options=pd.date_range(start=pd.to_datetime("2023-01-01"), end=pd.to_datetime("2023-12-31"), freq='D'),
        value=(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31"))
    )

    # Summary Cards
    st.write("### Summary")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(label="Total Stock", value="1000 Units")
    with col2:
        st.metric(label="Used Today", value="50 Units")
    with col3:
        st.metric(label="Received Today", value="200 Units")
    with col4:
        st.metric(label="Purchase Requests", value="3")
    with col5:
        st.metric(label="In Storage", value="150 Units")
    with col6:
        st.metric(label="Disposed", value="10 Units")

    # Inventory Change Over Time Graph
    st.write("### Inventory Change Over Time")
    data = np.random.randn(100, 2).cumsum(axis=0)
    plt.figure(figsize=(10, 6))
    plt.plot(data, label=["Stock", "Used"])
    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel("Units")
    st.pyplot(plt)

    # Detailed Data Table
    st.write("### Detailed Data")
    sample_data = {
        "Date": pd.date_range(start=pd.to_datetime("2023-01-01"), periods=10, freq='D'),
        "Category": ["Stock", "Used", "Received", "Purchase Request", "Storage", "Disposed"] * 2,
        "Quantity": np.random.randint(1, 100, size=10),
        "Expiry": pd.date_range(start=pd.to_datetime("2023-06-01"), periods=10, freq='D')
    }
    df = pd.DataFrame(sample_data)
    st.dataframe(df)
