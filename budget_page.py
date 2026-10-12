import streamlit as st
import data_loader

def init_categories():
    if "categories" not in st.session_state:
        st.session_state.categories = [
            "Food", "Transportation", "Utilities", "Savings", "Entertainment", "Miscellaneous"
        ]

        saved_budgets = data_loader.load_budget_data()
        
        if saved_budgets:
            existing_names = [cat.lower() for cat in st.session_state.categories]
            for entry in saved_budgets:
                cat_name = entry["category"]
                
                if cat_name.lower() not in existing_names:
                    st.session_state.categories.append(cat_name)
                    existing_names.append(cat_name.lower())

def show(selected_month_str=None):
    st.title("Monthly Budget Setup")
    
    init_categories()

    if selected_month_str:
        formatted_date = selected_month_str
    else:
        selected_month = st.session_state.get("selected_month", "January")
        selected_year = st.session_state.get("selected_year", "2027")
        formatted_date = f"{selected_month} {selected_year}"
    
    # Initialize session state for income list for the specific month
    income_state_key = f"incomes_{formatted_date}"
    if income_state_key not in st.session_state:
        all_budgets = data_loader.load_budget_data()
        month_budgets = [b for b in all_budgets if b["month"] == formatted_date] if all_budgets else []
        if month_budgets:
            seen_incomes = set()
            incomes_list = []
            for b in month_budgets:
                inc_tuple = (b["income_source"], b["income"])
                if inc_tuple not in seen_incomes:
                    seen_incomes.add(inc_tuple)
                    incomes_list.append({"source": b["income_source"], "amount": b["income"]})
            st.session_state[income_state_key] = incomes_list if incomes_list else [{"source": "Allowance", "amount": 15000.0}]
        else:
            st.session_state[income_state_key] = [{"source": "Allowance", "amount": 15000.0}]

    income_list = st.session_state[income_state_key]
    total_expected_income = sum(item["amount"] for item in income_list)
    combined_income_source = ", ".join(list(set(item["source"] for item in income_list))) if income_list else "None"

    all_budgets = data_loader.load_budget_data()
    if all_budgets is None:
        all_budgets = []
    current_month_budgets = [b for b in all_budgets if b["month"] == formatted_date]
    planned_map = {b["category"]: b["planned_amount"] for b in current_month_budgets}

    temp_planned_total = sum(planned_map.get(cat, 0.0) for cat in st.session_state.categories)
    temp_unallocated = total_expected_income - temp_planned_total

    st.subheader(f"Budget Summary ({formatted_date})")
    col1, col2, col3 = st.columns(3)
    
    col1.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: #f0f0f0;">💸 EXPECTED INCOME</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: #f0f0f0;">₱{total_expected_income:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
            
    plan_color = "#e56767" if temp_planned_total > total_expected_income else "#f0f0f0" # Red if exceeds
    col2.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: {plan_color};">📝 PLANNED EXPENSES</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: {plan_color};">₱{temp_planned_total:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
            
    if temp_unallocated >= 0:
        unalloc_color = "#72c472" # Pale green
        unalloc_icon = "✅"
    else:
        unalloc_color = "#e56767" # Pale red
        unalloc_icon = "⚠️"

    col3.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <p style="margin: 0; font-weight: 600; color: {unalloc_color};">{unalloc_icon} UNALLOCATED INCOME</p>
            <h3 style="margin: 0; padding-top: 0.5rem; color: {unalloc_color};">₱{temp_unallocated:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if temp_unallocated < 0:
        st.error(f"Warning: Your planned expenses exceed your expected income by ₱{abs(temp_unallocated):,.2f}!")

    st.write("---")
    st.subheader("Expected Income Sources")
    st.write("Manage your income sources and amounts for the month.")

    indices_to_remove_inc = []

    for idx, inc in enumerate(income_list):
        with st.container(border=True):
            col_src, col_amt, col_del = st.columns([4, 4, 2])
            
            col_src.text_input(f"Source_{idx}", value=inc["source"], key=f"inc_source_{formatted_date}_{idx}", label_visibility="collapsed", disabled=True)
            
            updated_amt = col_amt.number_input(
                f"Amt_{idx}", 
                min_value=0.0, 
                value=float(inc["amount"]), 
                step=500.0,
                key=f"inc_amt_{formatted_date}_{idx}",
                label_visibility="collapsed"
            )
            income_list[idx]["amount"] = updated_amt

            if col_del.button("Remove", key=f"del_inc_{formatted_date}_{idx}"):
                indices_to_remove_inc.append(idx)

    if indices_to_remove_inc:
        for idx in sorted(indices_to_remove_inc, reverse=True):
            st.session_state[income_state_key].pop(idx)
        st.rerun()

    # Add New Income 
    expander_inc = st.expander("➕ Add New Income Source")
    new_source = expander_inc.selectbox("Income Source", ["Allowance", "Salary", "Bonus", "Others"], key=f"new_income_source_input_{formatted_date}")
    new_amount = expander_inc.number_input("Amount (₱)", min_value=0.0, value=5000.0, step=500.0, key=f"new_income_amt_input_{formatted_date}")
    add_inc_clicked = expander_inc.button("Add Income Source", key=f"add_inc_btn_{formatted_date}")

    if add_inc_clicked:
        if new_amount > 0:
            st.session_state[income_state_key].append({"source": new_source, "amount": new_amount})
            st.success(f"Added '{new_source}' (₱{new_amount:,.2f}) successfully!")
            st.rerun()
        else:
            st.error("Income amount must be greater than 0.")

    st.write("---")
    st.subheader("Budget Categories & Planned Expenses")
    st.write("Rename categories, allocate funds, or remove buckets you don't need.")
    
    planned_budget = {}
    indices_to_remove_cat = []
    
    for i, category in enumerate(st.session_state.categories):
        with st.container(border=True):
            col_name, col_amt, col_del = st.columns([4, 4, 2])
            
            # Rename category 
            updated_name = col_name.text_input(f"Name_{i}", value=category, key=f"cat_name_{formatted_date}_{i}", label_visibility="collapsed")
            
            if updated_name.strip() and updated_name != category:
                st.session_state.categories[i] = updated_name.strip()
                
            current_name = st.session_state.categories[i]
            default_amt = planned_map.get(current_name, 0.0)

            # Allocate budget
            planned_amt = col_amt.number_input(
                f"Amt_{i}", 
                min_value=0.0, 
                value=float(default_amt), 
                step=100.0,
                key=f"budget_amt_{formatted_date}_{i}",
                label_visibility="collapsed"
            )
            planned_budget[current_name] = planned_amt
            
            # Remove category
            if col_del.button("Remove", key=f"del_cat_{formatted_date}_{i}"):
                indices_to_remove_cat.append(i)

    if indices_to_remove_cat:
        for idx in sorted(indices_to_remove_cat, reverse=True):
            st.session_state.categories.pop(idx)
        st.rerun()

    expander_cat = st.expander("➕ Add New Budget Category")
    new_cat_name = expander_cat.text_input("New Category Name", key=f"new_cat_input_{formatted_date}")
    add_cat_clicked = expander_cat.button("Add Category", key=f"add_cat_btn_{formatted_date}")
    
    if add_cat_clicked:
        name_exists = any(c.lower() == new_cat_name.strip().lower() for c in st.session_state.categories)
        if new_cat_name.strip() and not name_exists:
            st.session_state.categories.append(new_cat_name.strip())
            st.success(f"Added '{new_cat_name}' successfully!")
            st.rerun()
        elif name_exists:
            st.error("This category already exists.")
        else:
            st.error("Category name cannot be empty.")

    st.write("---")
    save_clicked = st.button("Save Budget", key=f"save_btn_{formatted_date}")
    
    if save_clicked:
        updated_budgets = [b for b in all_budgets if b["month"] != formatted_date]
        
        for category_name, amt in planned_budget.items():
            new_entry = {
                "month": formatted_date,
                "income_source": combined_income_source,
                "income": total_expected_income,
                "category": category_name,
                "planned_amount": amt
            }
            updated_budgets.append(new_entry)
            
        data_loader.save_budget_data(updated_budgets)
        st.success(f"Budget for {formatted_date} saved successfully!")