def usage_input_page():
    st.title("Usage Input")

    # File Uploader
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded File")
        st.dataframe(data)

        # Process the uploaded CSV
        # This is a placeholder for the logic to process the CSV and update the inventory
        # You'll need to implement the actual logic based on your CSV structure and inventory management rules

        # For demonstration, let's assume the CSV has columns ['Test Name', 'RI Used', 'RI Dose']
        # And we'll just display the 'RI Used' column for now
        used_RI = data['RI Used'].value_counts()
        st.write("### Processed Usage")
        st.dataframe(used_RI)
