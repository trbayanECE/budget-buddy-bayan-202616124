import streamlit as st
import dashboard_page, budget_page, expense_page
import data_loader

def get_financial_summary(month_filter):
    budget_entries = data_loader.load_budget_data()
    expense_entries = data_loader.load_expense_data()
    
    total_budget = 0.0
    total_expenses = 0.0
    
    if budget_entries:
        for entry in budget_entries:
            if entry["month"] == month_filter:
                total_budget += entry["planned_amount"]
            
    if expense_entries:
        for entry in expense_entries:
            if entry["month"] == month_filter:
                total_expenses += entry["amount"]
            
    remaining_total = total_budget - total_expenses
    
    return total_budget, total_expenses, remaining_total

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💸", layout="wide")

    st.sidebar.header("Budget Buddy")
    st.sidebar.markdown("*Know where your money goes*")

    months_list = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    years_list = [2026, 2027, 2028, 2029, 2030]

    selected_month_name = st.sidebar.selectbox("Select Month", months_list)
    selected_year = st.sidebar.selectbox("Select Year", years_list)

    selected_month = f"{selected_month_name} {selected_year}"
    
    st.session_state["selected_month"] = selected_month_name
    st.session_state["selected_year"] = str(selected_year)

    total_budget, total_expenses, remaining_total = get_financial_summary(selected_month)

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: #f0f0f0;">💰 BUDGET</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: #f0f0f0;">₱{total_budget:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
        
    col2.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: #f0f0f0;">📉 EXPENSES</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: #f0f0f0;">₱{total_expenses:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
        
    if remaining_total >= 0:
        rem_color = "#72c472" # Pale Green
        rem_icon = "✅"
    else:
        rem_color = "#e56767" # Pale Red
        rem_icon = "⚠️"
        
    col3.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: {rem_color};">{rem_icon} REMAINING TOTAL</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: {rem_color};">₱{remaining_total:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        /* Center tab headers */
        div[role="tablist"] {
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2, tab3 = st.tabs(["Budget", "Expenses", "Analysis"])

    with tab1:
        budget_page.show(selected_month)

    with tab2:
        expense_page.show()

    with tab3:
        dashboard_page.render_dashboard(selected_month)

main()