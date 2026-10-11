import streamlit as st

def show():
    st.title("Budget")
    st.write("Test:budget page_dropdown")
    selected_month = st.selectbox( "Select Month", 
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    income_source = st.selectbox( "Income Source", 
        ["Allowance", "Salary", "Bonus", "Others"] )
    expected_income = st.number_input("Expected Income (₱)", min_value=0.0, value=000.0, step=100.0)
    
    st.info(f"You selected {selected_month} with an expected income of ₱{expected_income:,.2f} from {income_source}.")
