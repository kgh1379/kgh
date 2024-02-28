# RI 사용일지
def ri_usage_log_page():
    st.title("RI Usage Log")

    # Display the log for the day
    # This is a placeholder for displaying the log
    # You'll need to fetch and display the actual log data from your database or log system
    st.write("### Daily Log")
    sample_log_data = {
        "Date": ["2023-09-01"],
        "Activity": ["Received"],
        "Details": ["Received 50 units of RI1"]
    }
    log_df = pd.DataFrame(sample_log_data)
    st.dataframe(log_df)
