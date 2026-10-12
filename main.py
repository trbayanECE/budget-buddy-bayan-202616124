import streamlit as st
import dashboard_page, budget_page, expense_page
import data_loader

def get_financial_summary(month_filter):
    budget_entries = data_loader.load_budget_data()
    expense_entries = data_loader.load_expense_data()
    
    total_budget = 0.0
    total_expenses = 0.0
    
    for entry in budget_entries:
        if entry["month"] == month_filter:
            total_budget += entry["planned_amount"]
            
    for entry in expense_entries:
        if entry["month"] == month_filter:
            total_expenses += entry["amount"]
            
    remaining_total = total_budget - total_expenses
    
    return total_budget, total_expenses, remaining_total

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💸", layout="centered")
    
    st.title("MyMoney - Budget Buddy")

    budget_entries = data_loader.load_budget_data()
    months = []
    for entry in budget_entries:
        if entry["month"] not in months:
            months.append(entry["month"])
            
    if not months:
        months = ["January 2027"]
        
    current_month = st.selectbox("Select Month", options=months)

    total_budget, total_expenses, remaining_total = get_financial_summary(current_month)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**BUDGET**\n\n### ₱{total_budget:,.2f}", icon="💰")
        
    with col2:
        st.info(f"**EXPENSES**\n\n### ₱{total_expenses:,.2f}", icon="📉")
        
    with col3:
        if remaining_total >= 0:
            st.success(f"**REMAINING TOTAL**\n\n### ₱{remaining_total:,.2f}", icon="✅")
        else:
            st.error(f"**REMAINING TOTAL**\n\n### ₱{remaining_total:,.2f}", icon="⚠️")

    tab1, tab2, tab3 = st.tabs(["Expenses", "Budget", "Analysis"])

    with tab1:
        expense_page.show()

    with tab2:
        budget_page.show()

    with tab3:
        dashboard_page.render_dashboard(current_month)

main()