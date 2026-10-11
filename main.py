import streamlit as st
import dashboard_page
import budget_page
import expense_page


st.set_page_config(
    page_title="Budget Buddy",
    page_icon="000",
    layout="wide"
)


st.sidebar.title("Budget Buddy")
st.sidebar.markdown("Test")

navigation = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Records", "Analysis", "Budgets", "Accounts", "Categories"]
)


if navigation == "Dashboard":
    dashboard_page.show()
elif navigation == "Budgets":
    budget_page.show()
elif navigation == "Records":
    expense_page.show()
elif navigation == "Analysis":
    st.title("Analysis")
    st.write("Advanced analysis and extra features will go here.")
elif navigation == "Accounts":
    st.title("Accounts")
    st.write("Account management view.")
elif navigation == "Categories":
    st.title("Categories")
    st.write("Category management view.")