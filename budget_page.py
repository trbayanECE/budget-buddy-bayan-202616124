import streamlit as st
import data_loader

def init_categories():
    if "categories" not in st.session_state:
        st.session_state.categories = [
            "Food", "Transportation", "Utilities", "Savings", "Entertainment", "Miscellaneous"
        ]
        
        saved_budgets = data_loader.load_budget_data()
        existing_names = [cat.lower() for cat in st.session_state.categories]
        
        for entry in saved_budgets:
            cat_name = entry["category"]
            if cat_name.lower() not in existing_names:
                st.session_state.categories.append(cat_name)
                existing_names.append(cat_name.lower())

def show():
    st.title("Monthly Budget Setup")
    
    init_categories()
    
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    years = ["2026", "2027", "2028", "2029", "2030"]
    
    col_m, col_y = st.columns(2)
    selected_month = col_m.selectbox("Select Month", months)
    selected_year = col_y.selectbox("Select Year", years)
    
    formatted_date = f"{selected_month} {selected_year}"
    
    income_source = st.selectbox("Income Source", ["Allowance", "Salary", "Bonus", "Others"])
    expected_income = st.number_input("Expected Income (₱)", min_value=0.0, value=15000.0, step=500.0)
    
    st.info(f"Setting budget for {formatted_date} with an expected income of ₱{expected_income:,.2f} from {income_source}.")

    st.write("---")
    st.subheader("Budget Categories & Planned Expenses")
    st.write("Rename categories, allocate funds, or remove buckets you don't need.")
    
    planned_budget = {}
    categories_to_delete = []

    for i, category in enumerate(st.session_state.categories):
        col_name, col_amt, col_del = st.columns([4, 4, 2])
        
        updated_name = col_name.text_input(f"Name_{i}", value=category, key=f"cat_name_{i}", label_visibility="collapsed")
        
        if updated_name.strip() and updated_name != category:
            st.session_state.categories[i] = updated_name.strip()
            
        current_name = st.session_state.categories[i]
        
        planned_amt = col_amt.number_input(
            f"Amt_{i}", 
            min_value=0.0, 
            value=0.0, 
            step=100.0,
            key=f"budget_{i}",
            label_visibility="collapsed"
        )
        planned_budget[current_name] = planned_amt
        
        delete_clicked = col_del.button("Remove", key=f"del_{i}")
        if delete_clicked:
            categories_to_delete.append(i)

    if categories_to_delete:
        for index in sorted(categories_to_delete, reverse=True):
            st.session_state.categories.pop(index)
        st.rerun()

    expander = st.expander("➕ Add New Budget Category")
    new_cat_name = expander.text_input("New Category Name")
    add_clicked = expander.button("Add Category")
    
    if add_clicked:
        name_exists = any(c.lower() == new_cat_name.strip().lower() for c in st.session_state.categories)
        if new_cat_name.strip() and not name_exists:
            st.session_state.categories.append(new_cat_name.strip())
            st.success(f"Added '{new_cat_name}' successfully!")
            st.rerun()
        elif name_exists:
            st.error("This category already exists.")
        else:
            st.error("Category name cannot be empty.")

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