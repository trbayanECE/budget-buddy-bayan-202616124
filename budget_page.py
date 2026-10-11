import streamlit as st
import data_loader

def init_categories():
    if "categories" not in st.session_state:
        st.session_state.categories = [
            {"name": "Food", "icon": "🍽️"},
            {"name": "Transportation", "icon": "🚗"},
            {"name": "Utilities", "icon": "📃"},
            {"name": "Savings", "icon": "🪙"},
            {"name": "Entertainment", "icon": "🎭"},
            {"name": "Miscellaneous", "icon": "☰"}
        ]

def show():
    st.title("Monthly Budget Setup")
    
    init_categories()
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    years = ["2026", "2027", "2028", "2029", "2030"]
    
    col1, col2 = st.columns(2)
    selected_month = col1.selectbox("Select Month", months)
    selected_year = col2.selectbox("Select Year", years)
    
    # combined month year
    formatted_date = f"{selected_month} {selected_year}"
    
    income_source = st.selectbox("Income Source", ["Allowance", "Salary", "Bonus", "Others"])
    expected_income = st.number_input("Expected Income (₱)", min_value=0.0, value=15000.0, step=500.0)
    
    st.info(f"Setting budget for {formatted_date} with an expected income of ₱{expected_income:,.2f} from {income_source}.")

    st.write("---")
    st.subheader("Budget Categories & Planned Expenses")
    st.write("Allocate your target budget across your custom categories below:")
    
    planned_budget = {}
    
    for cat in st.session_state.categories:
        category_name = cat["name"]
        category_icon = cat["icon"]
        
        planned_budget[category_name] = st.number_input(
            f"{category_icon} {category_name} (₱)", 
            min_value=0.0, 
            value=0.0, 
            step=100.0,
            key=f"budget_{category_name}"
        )

    total_planned = sum(planned_budget.values())
    unallocated = expected_income - total_planned

    st.write("---")
    st.subheader("Budget Summary")
    
    st.write(f"**Total Expected Income:** ₱{expected_income:,.2f}")
    st.write(f"**Total Planned Expenses:** ₱{total_planned:,.2f}")
    st.write(f"**Unallocated Income:** ₱{unallocated:,.2f}")
    
    if unallocated < 0:
        st.error(f"Warning: Your planned expenses exceed your expected income by ₱{abs(unallocated):,.2f}!")

    st.write("---")
    
    save_clicked = st.button("Save Budget")
    
    if save_clicked:
        all_budgets = data_loader.load_budget_data()
        
        updated_budgets = [b for b in all_budgets if b["month"] != formatted_date]
        
        for category_name, amt in planned_budget.items():
            new_entry = {
                "month": formatted_date,
                "income_source": income_source,
                "income": expected_income,
                "category": category_name,
                "planned_amount": amt
            }
            updated_budgets.append(new_entry)
            
        data_loader.save_budget_data(updated_budgets)
        st.success(f"Budget for {formatted_date} saved successfully!")