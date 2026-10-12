import streamlit as st
import dashboard_page, budget_page, expense_page
import data_loader

def get_financial_summary(month_filter):
    budget_entries = data_loader.load_budget_data()
    expense_entries = data_loader.load_expense_data()
    
    total_budget = 0.0
    total_expenses = 0.0
    
    # Sum of planned budget
    for entry in budget_entries:
        if entry["month"] == month_filter:
            total_budget += entry["planned_amount"]
            
    # Sum of recorded expenses 
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
        st.metric(label="BUDGET", value=f"₱{total_budget:,.2f}")
    with col2:
        st.metric(label="EXPENSES", value=f"₱{total_expenses:,.2f}")
    with col3:
        st.metric(label="REMAINING TOTAL", value=f"₱{remaining_total:,.2f}")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Expenses", "Budget", "Analysis"])

    with tab1:
        expense_page.show()

    with tab2:
        budget_page.show()

    with tab3:
        dashboard_page.render_dashboard(current_month)

main()