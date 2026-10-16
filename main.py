import streamlit as st
import dashboard_page
import budget_page
import expense_page

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💸", layout="wide")

    st.logo("assets/budgetbuddy_logo.png", size="large", icon_image="assets/budgetbuddy_icon.png") 

    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    
    months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    years_list = [2027, 2028, 2029, 2030, 2031]

    selected_month_name = st.sidebar.selectbox("Select Month", months_list)
    selected_year = st.sidebar.selectbox("Select Year", years_list)

    selected_month = f"{selected_month_name} {selected_year}"
    
    st.session_state["selected_month"] = selected_month_name
    st.session_state["selected_year"] = str(selected_year)

    st.sidebar.write("---")
    
    def run_budget():
        budget_page.show(selected_month)

    def run_expense():
        expense_page.show()

    def run_dashboard():
        dashboard_page.render_dashboard(selected_month)

    page_budget = st.Page(run_budget, title="Budget", icon="📔")
    page_expense = st.Page(run_expense, title="Expense", icon="🧾")
    page_dashboard = st.Page(run_dashboard, title="Analysis", icon="📊")

    pg = st.navigation([page_budget, page_expense, page_dashboard], position="hidden")

    st.sidebar.page_link(page_budget, label="Budget", icon="📔")
    st.sidebar.page_link(page_expense, label="Expense", icon="🧾")
    st.sidebar.page_link(page_dashboard, label="Analysis", icon="📊")

    pg.run()

main()