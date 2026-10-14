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

def render_metric_card(column, title, value, icon, text_color="#f0f0f0"):
    column.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: {text_color};">{icon} {title}</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: {text_color};">₱{value:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💸", layout="wide")

    st.sidebar.header("Budget Buddy")

    months_list = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    years_list = [2027, 2028, 2029, 2030, 2031]

    selected_month_name = st.sidebar.selectbox("Select Month", months_list)
    selected_year = st.sidebar.selectbox("Select Year", years_list)

    selected_month = f"{selected_month_name} {selected_year}"
    
    st.session_state["selected_month"] = selected_month_name
    st.session_state["selected_year"] = str(selected_year)

    total_budget, total_expenses, remaining_total = get_financial_summary(selected_month)

    col1, col2, col3 = st.columns(3)

    render_metric_card(col1, "BUDGET", total_budget, "💰")
        

    render_metric_card(col2, "Total EXPENSES", total_expenses, "📉")
        
    if remaining_total >= 0:
        rem_color = "#72c472"  # Pale Green
        rem_icon = "✅"
    else:
        rem_color = "#e56767"  # Pale Red
        rem_icon = "⚠️"
        
    render_metric_card(col3, "REMAINING TOTAL", remaining_total, rem_icon, text_color=rem_color)

    if total_budget > 0:
        progress_ratio = min(total_expenses / total_budget, 1.0)
    else:
        progress_ratio = 1.0 if total_expenses > 0 else 0.0

    if total_expenses <= total_budget:
        bar_color = "#72c472"  
    else:
        bar_color = "#e56767"  

    st.markdown(f"""
        <style>
        div[data-testid="stProgressBar"] > div > div > div {{
            background-color: {bar_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.progress(progress_ratio)
    st.markdown("")
    
    st.markdown(
    """
    <style>
    /* Centers the entire tab bar container */
    div[data-testid="stTabs"] [role="tablist"] {
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