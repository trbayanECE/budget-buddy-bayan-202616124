import streamlit as st
import dashboard_page
import budget_page
import expense_page

# Page configuration
st.set_page_config(
    page_title="Budget Buddy",
    page_icon="000",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Budget Buddy")
st.sidebar.markdown("Know where your money goes[cite: 1].")

navigation = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Budget Planner", "Expense Tracker"]
)

# Route to the selected page
if navigation == "Dashboard":
    dashboard_page.show()
elif navigation == "Budget Planner":
    budget_page.show()
elif navigation == "Expense Tracker":
    expense_page.show()