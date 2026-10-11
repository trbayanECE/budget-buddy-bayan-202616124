import streamlit as st

def show():
    st.title("Budget")
    st.write("Test:budget page_dropdown")
    selected_month = st.selectbox( "Select Month", 
        ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    income_source = st.selectbox( "Income Source", 
        ["Allowance", "Salary", "Bonus", "Others"] )
    expected_income = st.number_input("Expected Income (₱)", min_value=0.0, value=000.0, step=100.0)
    
    st.info(f"You selected {selected_month} with an expected income of ₱{expected_income:,.2f} from {income_source}.")

    st.write("---")
    st.subheader("Budget Categories & Planned Expenses")
    
    default_categories = [
        "Rent",
        "Biils",
        "Food",
        "Transportation",
        "Others"
    ]

    st.write("Allocate your target budget across the categories below:")
    
    planned_budget = {}
    
    for category in default_categories:
        planned_budget[category] = st.number_input(
            f"{category} (₱)", 
            min_value=0.0, 
            value=0.0, 
            step=100.0,
            key=category
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
