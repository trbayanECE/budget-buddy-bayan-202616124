import streamlit as st
import data_loader
from datetime import date

def init_expense_categories():
    if "categories" not in st.session_state:
        st.session_state.categories = [ "Food", "Transportation", "Utilities", "Savings", "Entertainment", "Miscellaneous"]
        
    saved_budgets = data_loader.load_budget_data()
    if saved_budgets:
        existing_names = [cat.lower() for cat in st.session_state.categories]
        for entry in saved_budgets:
            cat_name = entry["category"]
            if cat_name.lower() not in existing_names:
                st.session_state.categories.append(cat_name)
                existing_names.append(cat_name.lower())

def show():
    st.title("Expense Tracker", text_alignment="center")
    
    init_expense_categories()
    
    st.subheader("Record New Expense", text_alignment="center")

    st.write("---")
    
    col_date, col_month, col_year = st.columns([2, 2, 2])
    
    expense_date = col_date.date_input("Date", date.today())
    
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    years = ["2026", "2027", "2028", "2029", "2030"]
    
    default_month_idx = expense_date.month - 1
    default_year_idx = years.index(str(expense_date.year)) if str(expense_date.year) in years else 1
    
    selected_month = col_month.selectbox("Budget Month", months, index=default_month_idx)
    selected_year = col_year.selectbox("Budget Year", years, index=default_year_idx)
    
    formatted_month = f"{selected_month} {selected_year}"
    
    col_cat, col_amt = st.columns([2, 2])
    category = col_cat.selectbox("Category", st.session_state.categories)
    amount = col_amt.number_input("Amount (₱)", min_value=0.0, value=0.0, step=50.0)
    
    description = st.text_input("Description")

    st.write("---")
    
    if st.button("Save Expense", text_alignment="right"):
        if amount <= 0:
            st.error("Error: Expense amount must be greater than 0.")
        elif not description.strip():
            st.error("Error: Please complete description")
        else:
            st.success(f"Test Passed: Ready to save ₱{amount:,.2f} for {category} on {expense_date}.")

# Paalala to organize the code later pls tj