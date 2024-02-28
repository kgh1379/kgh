def stock_input_page():
    st.title("Stock Input")

    # Stock Input Form
    with st.form("Stock Input Form"):
        manufacturer = st.selectbox("Manufacturer", ["Manufacturer 1", "Manufacturer 2"])
        received_date = st.date_input("Received Date")
        lot_batch_no = st.text_input("Lot/Batch No")
        quantity = st.number_input("Quantity", min_value=1)
        receiver = st.text_input("Receiver")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Process and save the stock input
            # This is a placeholder for the logic to save the stock input to your database or inventory system
            st.success("Stock successfully added")
