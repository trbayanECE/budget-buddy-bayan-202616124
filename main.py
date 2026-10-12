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

    base_style = """
        height: 120px; 
        border-radius: 8px; 
        padding: 20px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center;
    """

    border_style = f"{base_style} border: 1px solid rgba(128, 128, 128, 0.4);"
    
    title_style = "font-size: 14px; font-weight: bold; opacity: 0.8; margin-bottom: 5px;"
    value_style = "font-size: 32px; font-weight: bold; line-height: 1.1;"

    with col1:
        st.markdown(f"""
        <div style="{border_style}">
            <div style="{title_style}">BUDGET</div>
            <div style="{value_style}">₱{total_budget:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="{border_style}">
            <div style="{title_style}">EXPENSES</div>
            <div style="{value_style}">₱{total_expenses:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        if remaining_total >= 0:
            bg_style = f"{base_style} background-color: #1a422b;" 
            text_color = "#5ee084" 
            icon = "✅"
        else:
            bg_style = f"{base_style} background-color: #4a1818;" 
            text_color = "#ff6b6b" 
            icon = "⚠️"
            
        st.markdown(f"""
        <div style="{bg_style} color: {text_color};">
            <div style="{title_style}">{icon} REMAINING TOTAL</div>
            <div style="{value_style}">₱{remaining_total:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Expenses", "Budget", "Analysis"])

    with tab1:
        expense_page.show()

    with tab2:
        budget_page.show()

    with tab3:
        dashboard_page.render_dashboard(current_month)

main()