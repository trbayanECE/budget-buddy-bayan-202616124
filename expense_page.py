import streamlit as st
import matplotlib.pyplot as plt
import data_loader
from datetime import date, datetime, timedelta
import calendar
import io

def init_expense_categories():
    """Initialize expense categories"""
    if "categories" not in st.session_state:
        st.session_state.categories = [
            "Food",
            "Transportation",
            "Utilities",
            "Savings",
            "Entertainment",
            "Miscellaneous",
        ]

    saved_budgets = data_loader.load_budget_data()
    if saved_budgets:
        existing_names = [cat.lower() for cat in st.session_state.categories]
        for entry in saved_budgets:
            cat_name = entry["category"]
            if cat_name.lower() not in existing_names:
                st.session_state.categories.append(cat_name)
                existing_names.append(cat_name.lower())


# record expense
def render_expense_form(months, years):
    with st.container(border=True):
        st.subheader("Record New Expense", text_alignment="center")

        col_date, col_month, col_year = st.columns(3)
        expense_date = col_date.date_input("Date", date.today())

        global_month = st.session_state.get(
            "selected_month", expense_date.strftime("%B")
        )
        global_year = st.session_state.get(
            "selected_year", str(expense_date.year)
        )

        default_month_idx = (
            months.index(global_month)
            if global_month in months
            else expense_date.month - 1
        )
        default_year_idx = (
            years.index(global_year) if global_year in years else 1
        )

        selected_month = col_month.selectbox(
            "Budget Month", months, index=default_month_idx
        )
        selected_year = col_year.selectbox(
            "Budget Year", years, index=default_year_idx
        )

        formatted_month = f"{selected_month} {selected_year}"

        col_cat, col_amt = st.columns(2)
        category = col_cat.selectbox("Category", st.session_state.categories)
        amount = col_amt.number_input(
            "Amount (₱)", min_value=0.0, value=0.0, step=50.0
        )

        description = st.text_input("Description")

        if st.button("Save Expense"):
            if amount <= 0:
                st.error("Error: Expense amount must be greater than 0.")
            elif not description.strip():
                st.error("Error: Please complete description")
            else:
                new_expense = {
                    "date": str(expense_date),
                    "month": formatted_month,
                    "category": category,
                    "description": description.strip(),
                    "amount": amount,
                }
                data_loader.add_expense(new_expense)
                st.success(
                    f"Successfully saved ₱{amount:,.2f} for {category} on {expense_date}!"
                )

    return selected_month, selected_year, formatted_month


# Date calculator helper
def build_date_context(selected_month, selected_year, months, years):
    all_possible_months = [f"{m} {y}" for y in years for m in months]

    month_idx = months.index(selected_month) + 1
    year_val = int(selected_year)
    num_days = calendar.monthrange(year_val, month_idx)[1]

    start_date = date(year_val, month_idx, 1)
    end_date = date(year_val, month_idx, num_days)

    weeks_in_month = []
    curr_d = start_date
    while curr_d <= end_date:
        yw = f"{curr_d.isocalendar()[0]}-W{curr_d.isocalendar()[1]:02d}"
        if yw not in weeks_in_month:
            weeks_in_month.append(yw)
        curr_d += timedelta(days=1)

    if not weeks_in_month:
        weeks_in_month = [f"{year_val}-W01"]

    return all_possible_months, start_date, end_date, weeks_in_month


def sync_history_state( global_month, global_year, all_possible_months, start_date):
    current_global = f"{global_month} {global_year}"
    if ("last_global_sync" not in st.session_state or st.session_state.last_global_sync != current_global):
        st.session_state.last_global_sync = current_global
        st.session_state.selected_history_month_idx = (all_possible_months.index(current_global)
            if current_global in all_possible_months
            else 0
        )
        st.session_state.selected_expense_day = start_date
        st.session_state.selected_week_idx = 0

    if "selected_history_month_idx" not in st.session_state:
        st.session_state.selected_history_month_idx = 0
    if "selected_expense_day" not in st.session_state:
        st.session_state.selected_expense_day = start_date
    if "selected_week_idx" not in st.session_state:
        st.session_state.selected_week_idx = 0


def filter_active_expenses(history_view, all_expenses, month_filtered_expenses, all_possible_months, weeks_in_month):
    """Filters expenses based on the selected view"""
    if history_view == "Month":
        active_label = all_possible_months[
            st.session_state.selected_history_month_idx
        ]
        active_expenses = [
            exp for exp in all_expenses if exp.get("month") == active_label
        ]
    elif history_view == "Weekly":
        active_label = weeks_in_month[st.session_state.selected_week_idx]
        active_expenses = []
        for exp in month_filtered_expenses:
            dt_obj = datetime.strptime(exp["date"], "%Y-%m-%d")
            yw = f"{dt_obj.isocalendar()[0]}-W{dt_obj.isocalendar()[1]:02d}"
            if yw == active_label:
                active_expenses.append(exp)
    else:
        active_label = str(st.session_state.selected_expense_day)
        active_expenses = [
            exp
            for exp in month_filtered_expenses
            if exp["date"] == active_label
        ]

    return active_label, active_expenses


def render_prev_next_buttons(history_view, col_prev, col_next, all_possible_months, weeks_in_month, start_date, end_date):
    with col_prev:
        if history_view == "Month":
            if st.button("◀", key="prev_month_btn", use_container_width=True):
                if st.session_state.selected_history_month_idx > 0:
                    st.session_state.selected_history_month_idx -= 1
        elif history_view == "Weekly":
            if st.button("◀", key="prev_week_btn", use_container_width=True):
                if st.session_state.selected_week_idx > 0:
                    st.session_state.selected_week_idx -= 1
        else:
            if st.button("◀", key="prev_day_btn", use_container_width=True):
                new_day = st.session_state.selected_expense_day - timedelta(
                    days=1
                )
                if new_day >= start_date:
                    st.session_state.selected_expense_day = new_day

    with col_next:
        if history_view == "Month":
            if st.button("▶", key="next_month_btn", use_container_width=True):
                if (st.session_state.selected_history_month_idx < len(all_possible_months) - 1):
                    st.session_state.selected_history_month_idx += 1
        elif history_view == "Weekly":
            if st.button("▶", key="next_week_btn", use_container_width=True):
                if (st.session_state.selected_week_idx < len(weeks_in_month) - 1):
                    st.session_state.selected_week_idx += 1
        else:
            if st.button("▶", key="next_day_btn", use_container_width=True):
                new_day = st.session_state.selected_expense_day + timedelta(
                    days=1
                )
                if new_day <= end_date:
                    st.session_state.selected_expense_day = new_day


def render_summary_cards(col_mid, col_total, active_label, period_total):
    with col_mid:
        st.markdown(
            f"""
            <div style="background-color: #363531; border: 1px solid #5e5c56; border-radius: 8px; height: 68px; display: flex; align-items: center; justify-content: center; box-sizing: border-box; text-align: center;">
                <span style="color: #f0f0f0; font-size: 35px; font-weight: bold;">{active_label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_total:
        st.markdown(
            f"""
            <div style="background-color: #363531; border: 1px solid #5e5c56; border-radius: 8px; height: 68px; padding: 6px 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-sizing: border-box; text-align: center;">
                <div style="color: #a3a3a3; font-size: 15px; font-weight: 600; letter-spacing: 0.5px;">📉 TOTAL SPENT</div>
                <div style="color: #e56767; font-size: 28px; font-weight: bold;">₱{period_total:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_expense_table(active_expenses, active_label):
    if not active_expenses:
        st.info(f"No expenses recorded for {active_label}.")
    else:
        display_data = []
        for exp in reversed(active_expenses):
            display_data.append({
                "Date": exp["date"],
                "Category": exp["category"],
                "Description": exp["description"],
                "Amount": f"₱{exp['amount']:,.2f}",
            })
        st.dataframe(display_data, use_container_width=True, hide_index=True)


def render_spending_analytics(all_expenses, month_filtered, history_view, active_label, formatted_month):
    if history_view == "Month":
        year = active_label.split()[1] if " " in active_label else active_label
        st.header(f"Spending Analytics for {year}", text_alignment="center")
        
        totals = {}
        months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        for m in months_order:
            totals[m] = 0.0
            
        has_data = False
        for exp in all_expenses:
            if exp.get("month", "").endswith(year):
                m = exp["month"].split()[0]
                if m in totals:
                    totals[m] += exp["amount"]
                    has_data = True
                    
        x_vals = months_order
        y_vals = [totals[m] for m in x_vals]
        x_axis_label = "Month"
        
    elif history_view == "Weekly":
        st.header(f"Spending Analytics for {formatted_month}", text_alignment="center")
        totals = {}
        for exp in month_filtered:
            dt_obj = datetime.strptime(exp["date"], "%Y-%m-%d")
            yw = f"{dt_obj.isocalendar()[0]}-W{dt_obj.isocalendar()[1]:02d}"
            totals[yw] = totals.get(yw, 0.0) + exp["amount"]
            
        x_vals = sorted(totals.keys())
        y_vals = [totals[w] for w in x_vals]
        x_axis_label = "Week"
        has_data = len(x_vals) > 0
        
    else: # daily
        st.header(f"Spending Analytics for {formatted_month}", text_alignment="center")
        totals = {}
        for exp in month_filtered:
            d = exp["date"]
            totals[d] = totals.get(d, 0.0) + exp["amount"]
            
        x_vals = sorted(totals.keys())
        y_vals = [totals[d] for d in x_vals]
        x_axis_label = "Date"
        has_data = len(x_vals) > 0

    if not has_data:
        st.info("No expense data available to display chart.")
        return

    rainbow_palette = ["#ff4b4b", "#ffa15a", "#f6c915", "#72c472", "#29b5e8", "#ab63fa", "#e56767", ]
    bar_colors = [rainbow_palette[i % len(rainbow_palette)] for i in range(len(x_vals))]

    fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
    ax.set_facecolor("none")

    ax.bar(x_vals, y_vals, color=bar_colors)
    ax.set_xlabel(x_axis_label, color="white")
    ax.set_ylabel("Amount (₱)", color="white")
    plt.xticks(rotation=45, ha="right", color="white")
    plt.yticks(color="white")

    for spine in ax.spines.values():
        spine.set_color("#5e5c56")

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(
        buf, format="png", transparent=True, dpi=300, bbox_inches="tight"
    )
    st.image(buf)
    plt.close(fig)


def show():
    st.header("Expense Tracker", text_alignment="center", divider="rainbow")

    init_expense_categories()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",]
    years = ["2026", "2027", "2028", "2029", "2030", "2031"]

    controls_container = st.container()

    col_left, col_right = st.columns([1.5, 1], gap="small")

    with col_right:
        selected_month, selected_year, formatted_month = render_expense_form(
            months, years
        )

    all_expenses = data_loader.load_expense_data()
    month_filtered = [
        exp for exp in all_expenses if exp.get("month") == formatted_month
    ]

    all_possible_months, start_date, end_date, weeks_in_month = (
        build_date_context(selected_month, selected_year, months, years)
    )

    global_month = st.session_state.get("selected_month", selected_month)
    global_year = st.session_state.get("selected_year", selected_year)
    sync_history_state(
        global_month, global_year, all_possible_months, start_date
    )

    with controls_container:
        col_view, col_prev, col_mid, col_next, col_total = st.columns(
            [2.2, 0.4, 3.8, 0.4, 2.6], vertical_alignment="center"
        )

        with col_view:
            history_view = st.radio(
                "VIEW HISTORY BY:",
                ["Month", "Weekly", "Daily"],
                horizontal=True,
                key="expense_history_view",
            )

        active_label, active_expenses = filter_active_expenses(
            history_view,
            all_expenses,
            month_filtered,
            all_possible_months,
            weeks_in_month,
        )
        period_total = sum(exp["amount"] for exp in active_expenses)

        render_prev_next_buttons(
            history_view,
            col_prev,
            col_next,
            all_possible_months,
            weeks_in_month,
            start_date,
            end_date,
        )
        render_summary_cards(col_mid, col_total, active_label, period_total)

    with col_left:
        display_expense_table(active_expenses, active_label)

    st.write("---")
    
    render_spending_analytics(all_expenses, month_filtered, history_view, active_label, formatted_month)