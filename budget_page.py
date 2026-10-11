import streamlit as st

def show():
    st.title("Budget")
    st.write("Test:Monthly dropdown")

selected_month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

