import streamlit as st
import dashboard_page
import budget_page
import expense_page


st.set_page_config(
    page_title="Budget Buddy",
    page_icon="💸",
    layout="wide"
)


st.sidebar.title("Budget Buddy")
st.sidebar.markdown("Test")

navigation = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Records", "Budget", "Analysis", "Accounts", "Categories"]
)


if navigation == "Dashboard":
    dashboard_page.show()
elif navigation == "Budgets":
    budget_page.show()
elif navigation == "Records":
    expense_page.show()
elif navigation == "Analysis":
    st.title("Analysis")
    st.write("Pie charts and percentages ")
elif navigation == "Accounts":
    st.title("Accounts")
    st.write("Accounts management")
elif navigation == "Categories":
    st.title("Categories")
    st.write("Expense and income category lists")