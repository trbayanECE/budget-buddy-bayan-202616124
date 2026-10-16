import streamlit as st
import data_loader

def init_categories():
    if "categories" not in st.session_state:
        st.session_state.categories = ["Food", "Transportation", "Utilities", "Savings", "Entertainment", "Miscellaneous"]
        saved_budgets = data_loader.load_budget_data()
        
        if saved_budgets:
            existing_names = [cat.lower() for cat in st.session_state.categories]
            for entry in saved_budgets:
                cat_name = entry["category"]
                if cat_name.lower() not in existing_names:
                    st.session_state.categories.append(cat_name)
                    existing_names.append(cat_name.lower())

def init_incomes(formatted_date, all_budgets):
    income_state_key = f"incomes_{formatted_date}"
    if income_state_key not in st.session_state:
        month_budgets = [b for b in all_budgets if b["month"] == formatted_date] if all_budgets else []
        if month_budgets:
            incomes_list = []
            source_str = month_budgets[0].get("income_source", "")
            
            if "::" in source_str:
                for part in source_str.split("||"):
                    if "::" in part:
                        s, a = part.split("::")
                        incomes_list.append({"source": s, "amount": float(a)})
            else:
                seen_incomes = set()
                for b in month_budgets:
                    inc_tuple = (b["income_source"], b["income"])
                    if inc_tuple not in seen_incomes:
                        seen_incomes.add(inc_tuple)
                        incomes_list.append({"source": b["income_source"], "amount": b["income"]})
                        
            st.session_state[income_state_key] = incomes_list if incomes_list else [{"source": "Allowance", "amount": 0.0}]
        else:
            st.session_state[income_state_key] = [{"source": "Allowance", "amount": 0.0}]
    return income_state_key

def calculate_totals(formatted_date, income_list, planned_map):
    total_expected_income = 0.0
    for idx, inc in enumerate(income_list):
        amt_key = f"inc_amt_{formatted_date}_{idx}"
        val = float(st.session_state[amt_key]) if amt_key in st.session_state else float(inc["amount"])
        total_expected_income += val
        inc["amount"] = val 

    temp_planned_total = 0.0
    for i, category in enumerate(st.session_state.categories):
        amt_key = f"budget_amt_{formatted_date}_{i}"
        val = float(st.session_state[amt_key]) if amt_key in st.session_state else float(planned_map.get(category, 0.0))
        temp_planned_total += val
        
    temp_unallocated = total_expected_income - temp_planned_total
    
    combined_income_source = "||".join([f"{item['source']}::{item['amount']}" for item in income_list]) if income_list else "None"
    
    return total_expected_income, temp_planned_total, temp_unallocated, combined_income_source

def display_summary_cards(total_expected_income, temp_planned_total, temp_unallocated):
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem;">💸 EXPECTED INCOME</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #f0f0f0;">₱{total_expected_income:,.2f}</div>
        </div>""", unsafe_allow_html=True)

    plan_color = "#e56767" if temp_planned_total > total_expected_income else "#f0f0f0"
    col2.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: {plan_color}; margin-bottom: 0.5rem;">📝 PLANNED EXPENSES</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {plan_color};">₱{temp_planned_total:,.2f}</div>
        </div>""", unsafe_allow_html=True)

    unalloc_color = "#72c472" if temp_unallocated >= 0 else "#e56767"
    unalloc_icon = "✅" if temp_unallocated >= 0 else "⚠️"
    col3.markdown(f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: {unalloc_color}; margin-bottom: 0.5rem;">{unalloc_icon} UNALLOCATED</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {unalloc_color};">₱{temp_unallocated:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    
    if temp_unallocated < 0:
        st.error(f"Warning: Your planned expenses exceed your expected income by ₱{abs(temp_unallocated):,.2f}!")
    st.write("")

def display_budget_progress_bar(total_expected_income, temp_unallocated, formatted_date, planned_map, colors):
    if total_expected_income <= 0:
        return
        
    bar_segments = []
    for idx, cat in enumerate(st.session_state.categories):
        amt_key = f"budget_amt_{formatted_date}_{idx}"
        cat_amt = float(st.session_state[amt_key]) if amt_key in st.session_state else float(planned_map.get(cat, 0.0))
        pct = (cat_amt / total_expected_income) * 100
        if pct > 0:
            bar_segments.append(f'<div style="width: {pct:.2f}%; background-color: {colors[idx % len(colors)]}; height: 20px;" title="{cat}: ₱{cat_amt:,.2f} ({pct:.1f}%)"></div>')
    
    if temp_unallocated > 0:
        unalloc_pct = (temp_unallocated / total_expected_income) * 100
        bar_segments.append(f'<div style="width: {unalloc_pct:.2f}%; background-color: #5e5c56; height: 20px;" title="Unallocated: ₱{temp_unallocated:,.2f} ({unalloc_pct:.1f}%)"></div>')

    st.markdown(f"""
    <div style="display: flex; width: 100%; height: 20px; background-color: #363531; border-radius: 5px; overflow: hidden; margin-bottom: 12px; border: 1px solid #5e5c56;">
        {"".join(bar_segments) if bar_segments else '<div style="width: 100%; background-color: #5e5c56; height: 20px;"></div>'}
    </div>
    """, unsafe_allow_html=True)
    st.write("")

def manage_budget_categories(formatted_date, planned_map, total_expected_income, colors):
    planned_budget = {}
    indices_to_remove_cat = []
    cat_cols = st.columns(2)
    
    for i, category in enumerate(st.session_state.categories):
        target_col = cat_cols[i % 2]
        color = colors[i % len(colors)]
        
        with target_col.container(border=True):
            sub_col_name, sub_col_amt, sub_col_del = st.columns([4, 4, 3])
            
            updated_name = sub_col_name.text_input(f"Name_{i}", value=category, key=f"cat_name_{formatted_date}_{i}", label_visibility="collapsed")
            if updated_name.strip() and updated_name != category:
                st.session_state.categories[i] = updated_name.strip()
                
            current_name = st.session_state.categories[i]
            default_amt = planned_map.get(current_name, 0.0)

            planned_amt = sub_col_amt.number_input(f"Amt_{i}", min_value=0.0, value=float(default_amt), step=100.0, key=f"budget_amt_{formatted_date}_{i}", label_visibility="collapsed")
            planned_budget[current_name] = planned_amt
            
            if sub_col_del.button("Remove", key=f"del_cat_{formatted_date}_{i}", use_container_width=True):
                indices_to_remove_cat.append(i)

            cat_pct = (planned_amt / total_expected_income) * 100 if total_expected_income > 0 else 0.0
            st.markdown(f"""
            <div style="width: 100%; background-color: #363531; border-radius: 4px; height: 8px; margin-top: 5px;">
                <div style="width: {min(cat_pct, 100)}%; background-color: {color}; height: 8px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #a0a0a0; margin-top: 4px;">{cat_pct:.1f}% of planned income</div>
            """, unsafe_allow_html=True)

    if indices_to_remove_cat:
        for idx in sorted(indices_to_remove_cat, reverse=True):
            st.session_state.categories.pop(idx)
        st.rerun()

    with st.expander("➕ Add New Budget Category"):
        new_cat_name = st.text_input("New Category Name", key=f"new_cat_input_{formatted_date}")
        if st.button("Add Category", key=f"add_cat_btn_{formatted_date}"):
            if new_cat_name.strip() and not any(c.lower() == new_cat_name.strip().lower() for c in st.session_state.categories):
                st.session_state.categories.append(new_cat_name.strip())
                st.success(f"Added '{new_cat_name}' successfully!")
                st.rerun()
            else:
                st.error("Category name is empty or already exists.")
                
    return planned_budget

def manage_income_sources(formatted_date, income_state_key, income_list):
    st.write("---")
    st.subheader("Expected Income Sources", text_alignment="center")
    
    indices_to_remove_inc = []
    for idx, inc in enumerate(income_list):
        with st.container(border=True):
            col_src, col_amt, col_del = st.columns([4, 4, 2])
            col_src.text_input(f"Source_{idx}", value=inc["source"], key=f"inc_source_{formatted_date}_{idx}", label_visibility="collapsed", disabled=True)
            col_amt.number_input(f"Amt_{idx}", min_value=0.0, value=float(inc["amount"]), step=500.0, key=f"inc_amt_{formatted_date}_{idx}", label_visibility="collapsed")
            if col_del.button("Remove", key=f"del_inc_{formatted_date}_{idx}", use_container_width=True):
                indices_to_remove_inc.append(idx)

    if indices_to_remove_inc:
        for idx in sorted(indices_to_remove_inc, reverse=True):
            st.session_state[income_state_key].pop(idx)
        st.rerun()

    with st.expander("➕ Add New Income Source"):
        new_source = st.selectbox("Income Source", ["Allowance", "Salary", "Bonus", "Others"], key=f"new_income_source_input_{formatted_date}")
        new_amount = st.number_input("Amount (₱)", min_value=0.0, value=5000.0, step=500.0, key=f"new_income_amt_input_{formatted_date}")
        if st.button("Add Income Source", key=f"add_inc_btn_{formatted_date}"):
            if new_amount > 0:
                st.session_state[income_state_key].append({"source": new_source, "amount": new_amount})
                st.success(f"Added '{new_source}' (₱{new_amount:,.2f}) successfully!")
                st.rerun()
            else:
                st.error("Income amount must be greater than 0.")

    st.write("---")

def save_budget(formatted_date, all_budgets, planned_budget, combined_income_source, total_expected_income):
    if st.button("Save Budget", type="primary", key=f"save_btn_{formatted_date}"):
        updated_budgets = [b for b in all_budgets if b["month"] != formatted_date]
        for category_name, amt in planned_budget.items():
            updated_budgets.append({
                "month": formatted_date,
                "income_source": combined_income_source,
                "income": total_expected_income,
                "category": category_name,
                "planned_amount": amt
            })
        data_loader.save_budget_data(updated_budgets)
        st.success(f"Budget for {formatted_date} saved successfully!")


def show(selected_month_str=None):
    init_categories()
    
    formatted_date = selected_month_str or f"{st.session_state.get('selected_month', 'January')} {st.session_state.get('selected_year', '2027')}"
    all_budgets = data_loader.load_budget_data() or []
    
    income_state_key = init_incomes(formatted_date, all_budgets)
    income_list = st.session_state[income_state_key]
    current_month_budgets = [b for b in all_budgets if b["month"] == formatted_date]
    planned_map = {b["category"]: b["planned_amount"] for b in current_month_budgets}

    total_expected_income, temp_planned_total, temp_unallocated, combined_income_source = calculate_totals(
        formatted_date, income_list, planned_map
    )
    st.header(f"({formatted_date}) Budget Categories & Planned Expenses", text_alignment="center", divider="rainbow")
    display_summary_cards(total_expected_income, temp_planned_total, temp_unallocated)
    
    colors = ["#ff4b4b","#ffa15a","#f6c915","#72c472","#29b5e8","#ab63fa","#e56767","#ff758f","#e84393","#ff9eae","#ff7f0e","#ffc857","#ffe66d","#2ecc71","#00b894",]
    display_budget_progress_bar(total_expected_income, temp_unallocated, formatted_date, planned_map, colors)
    
    planned_budget = manage_budget_categories(formatted_date, planned_map, total_expected_income, colors)
    manage_income_sources(formatted_date, income_state_key, income_list)
    save_budget(formatted_date, all_budgets, planned_budget, combined_income_source, total_expected_income)