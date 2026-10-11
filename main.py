import streamlit as st
import dashboard_page, budget_page, expense_page

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💸", layout="centered")
    
    st.title("MyMoney - Budget Buddy", text_alignment="center")

    tab1, tab2, tab3 = st.tabs(["Dashboard", "Budget Planner", "Expense Tracker"])
    
    with tab1:
        dashboard_page.show()
        
    with tab2:
        budget_page.show()
        
    with tab3:
        expense_page.show()

main()

#https://docs.streamlit.io/develop/api-reference/layout/st.tabs

