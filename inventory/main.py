import streamlit as st
import gdatabase as db
from datetime import datetime, timedelta
# from python_docx import Document
from docx.shared import Pt
import pythoncom

def app():
    st.sidebar.title("BRMH NM")
    category = st.sidebar.radio("RI", ["Mo-99 Generator", "방사성동위원소&의약품"])

    # Generator Section
    if category == "Mo-99 Generator":
        generator_option = st.sidebar.selectbox("선택", ["입고 입력", "재고 현황", "출고 입력", "출고 현황"])
        
        if generator_option == "입고 입력":
            # Display Receipt functionality
            with st.form("Receipt Form"):
                manufacturer = st.selectbox("제조사", ["Mallin", "Samyong"])
                acquisition_date = st.date_input("취득일자")
                acquisition_date_str = acquisition_date.strftime("%Y-%m-%d")
                lot_batch_no = st.text_input("Lot/Batch No")
                receiver = st.text_input("수령인")
                submitted = st.form_submit_button("저장")
                added_days = acquisition_date + timedelta(days=80)
                expected_dispatch_date = added_days.strftime("%Y-%m-%d")
                
            if submitted:
                receipt_data = {
                    "manufacturer": manufacturer,
                    "acquisition_date": acquisition_date_str,
                    "lot_batch_no": lot_batch_no,
                    "receiver": receiver,
                    "expected_dispatch_date": expected_dispatch_date
                }
                db.insert_receipt(receipt_data)
                st.success("Receipt Submitted")

        elif generator_option == "재고 현황":
        # Allow selection of a manufacturer
            manufacturer_selected = st.selectbox("제조사 선택", ["All","Mallin", "Samyong"])

        # Fetch and display the unshipped generators for the selected manufacturer
            if manufacturer_selected == "All":
                unshipped_generators = db.get_unshipped_generators_all()
            else:
                unshipped_generators = db.get_unshipped_generators_by_manufacturer(manufacturer_selected)

            if unshipped_generators:
                st.write("Unshipped Generators:")
                for generator in unshipped_generators:
                    st.text(f"Manufacturer: {generator[4]}, Acquisition Date: {generator[0]}, Lot/Batch No: {generator[1]}, Consignee: {generator[2]}, Expected Delivery Date: {generator[3]}")
            else:
                st.write("No unshipped generators found for the selected option.")

        elif generator_option == "출고 입력":
            # Display Shipment Input functionality
            with st.form("Dispatch Form"):
                receipt_id = st.selectbox("제조사", options=db.get_available_generators())
                dispatch_date = st.date_input("출고일")
                radiation_dose_rate_dispatch = st.text_input("방사선량율 (uSv/hr)")
                checker = st.text_input("확인자")
                submitted = st.form_submit_button("출고 저장")
                if submitted:
                    dispatch_data = {
                        "제조사": manufacturer,
                        "출고일": dispatch_date,
                        "방사선량율 (usv/hr)": radiation_dose_rate_dispatch,
                        "확인자": checker,
                        "expected_dispatch_date": expected_dispatch_date
                    }
                    db.insert_dispatch(dispatch_data)
                    st.success("Dispatch Submitted")

        elif generator_option == "출고 현황":
            # Display Shipment Status functionality
            dispatches = db.get_dispatches()
            st.write("출고현황:", dispatches)

    # RI&RP Section
    elif category == "방사성동위원소&의약품":
        ri_rp_option = st.sidebar.selectbox("선택", ["재고 현황", "입고 입력", "사용 입력", "보관", "폐기"])

        if ri_rp_option == "재고 현황":
            # Display Inventory Status functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("재고 현황 + 자동 구매요청 수량에 맞춰 기사장에게 메시지 자동발송")

        elif ri_rp_option == "입고 입력":
            # Display In Stock functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("In Stock: 사용자가 직접 입력 or 바코드 입력기능 활용")

        elif ri_rp_option == "사용 입력":
            # Display Usage functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("csv파일 불러와서 Vial, RI dose 자동 완성")

        elif ri_rp_option == "구매 요청":
            # Display Purchase Request functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("구매 요청하면 기사장에서 메시지")
        
        elif ri_rp_option == "보관":
            # Display Purchase Request functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("사용하지 않고 보관중인 RI(필터 역할)")
        
        elif ri_rp_option == "폐기":
            # Display Purchase Request functionality
            # (Implement similar to Generator section with corresponding database functions)
            st.write("보관중 폐기된 RI")

if __name__ == "__main__":
    db.create_tables()
    app()