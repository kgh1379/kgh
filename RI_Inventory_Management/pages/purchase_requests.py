def purchase_request_page():
    st.title("Purchase Request")

    # Display items that need restocking
    # This is a placeholder for the actual logic to determine which items need restocking
    st.write("### Items Needing Restock")
    restock_items = {
        "RI Name": ["RI1", "RI2"],
        "Current Quantity": [10, 25],
        "Minimum Required": [20, 30]
    }
    restock_df = pd.DataFrame(restock_items)
    st.dataframe(restock_df)

    #
