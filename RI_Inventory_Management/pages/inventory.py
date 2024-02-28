def inventory_page():
    st.title("Inventory Status")

    # Inventory Table
    st.write("### RI List")
    inventory_data = {
        "RI Name": ["RI1", "RI2", "RI3"],
        "Quantity": [100, 50, 75],
        "Expiry Date": ["2023-12-31", "2023-11-30", "2024-01-15"],
        "Alert Quantity": [20, 30, 25]
    }
    inventory_df = pd.DataFrame(inventory_data)
    st.dataframe(inventory_df)

    # Check for Low Stock and Send Alerts
    low_stock_items = inventory_df[inventory_df["Quantity"] <= inventory_df["Alert Quantity"]]
    if not low_stock_items.empty:
        st.write("### Low Stock Alerts")
        st.dataframe(low_stock_items)
        # Here, integrate with your notification system to send alerts
