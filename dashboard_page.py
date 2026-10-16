import matplotlib.pyplot as plt
import streamlit as st
import data_loader


def build_category_summary(selected_month, budget_entries, expense_entries):
    summary = {}
    for bud in budget_entries:
        if bud.get("month") == selected_month:
            cat = bud["category"]
            if cat not in summary:
                summary[cat] = {"planned": 0.0, "actual": 0.0}
            summary[cat]["planned"] += float(bud.get("planned_amount", 0.0))

    for exp in expense_entries:
        if exp.get("month") == selected_month:
            cat = exp["category"]
            if cat not in summary:
                summary[cat] = {"planned": 0.0, "actual": 0.0}
            summary[cat]["actual"] += float(exp.get("amount", 0.0))

    return summary


def calculate_financial_metrics(selected_month, budget_entries, category_summary):
    total_income = 0.0
    for bud in budget_entries:
        if bud.get("month") == selected_month:
            total_income = float(bud.get("income", 0.0))
            break

    total_planned = sum(item["planned"] for item in category_summary.values())
    total_actual = sum(item["actual"] for item in category_summary.values())
    money_remaining = total_income - total_actual

    return total_income, total_planned, total_actual, money_remaining


def render_financial_summary(total_income, total_planned, total_actual, money_remaining):
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(
        f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem;">💰 TOTAL INCOME</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #f0f0f0;">₱{total_income:,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    col2.markdown(
        f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem;">📋 PLANNED EXPENSES</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #f0f0f0;">₱{total_planned:,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    col3.markdown(
        f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem;">🧾 ACTUAL EXPENSES</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #f0f0f0;">₱{total_actual:,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    rem_color = "#72c472" if money_remaining >= 0 else "#e56767"
    rem_icon = "🪙" if money_remaining >= 0 else "⚠️"
    col4.markdown(
        f"""
        <div style="background-color: #363531; padding: 1rem; border-radius: 0.5rem; border: 1px solid #5e5c56;">
            <div style="font-size: 0.85rem; font-weight: 600; color: {rem_color}; margin-bottom: 0.5rem;">{rem_icon} MONEY REMAINING</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: {rem_color};">₱{money_remaining:,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def render_pie_chart(category_summary):
    plt.style.use("dark_background")
    labels = []
    sizes = []

    for cat, amounts in category_summary.items():
        if amounts["planned"] > 0:
            labels.append(cat)
            sizes.append(amounts["planned"])

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    if sizes:
        max_idx = sizes.index(max(sizes))
        explode = [0.1 if i == max_idx else 0 for i in range(len(sizes))]
        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            autopct="%1.1f%%",
            shadow=True,
            startangle=90,
        )
        ax.axis("equal")
    else:
        ax.text(0.5, 0.5, "No planned budget data", ha="center", va="center")
        ax.axis("off")

    return fig


def render_comparison_chart(category_summary):
    plt.style.use("dark_background")
    categories = list(category_summary.keys())
    planned = [category_summary[cat]["planned"] for cat in categories]
    actual = [category_summary[cat]["actual"] for cat in categories]

    x = range(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    if categories:
        ax.bar(
            [i - width / 2 for i in x],
            planned,
            width,
            label="Planned",
            color="#00d4ff",
        )
        ax.bar(
            [i + width / 2 for i in x],
            actual,
            width,
            label="Actual",
            color="#ff6666",
        )
        ax.set_ylabel("Amount (₱)")
        ax.set_title("Planned vs Actual Spending")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")
        legend = ax.legend()
        legend.get_frame().set_alpha(0.0)
    else:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        ax.axis("off")

    plt.tight_layout()
    return fig


def render_charts_section(category_summary):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<p style='text-align: center; font-weight: bold;'>Planned Budget Distribution</p>",
            unsafe_allow_html=True,
        )
        fig_pie = render_pie_chart(category_summary)
        st.pyplot(fig_pie)
        plt.close(fig_pie)

    with col2:
        st.markdown(
            "<p style='text-align: center; font-weight: bold;'>Planned vs Actual Spending</p>",
            unsafe_allow_html=True,
        )
        fig_bar = render_comparison_chart(category_summary)
        st.pyplot(fig_bar)
        plt.close(fig_bar)


def render_budget_breakdown(category_summary):
    st.header("Budget Breakdown", text_alignment="center")

    if not category_summary:
        st.info("No data available.")
        return

    with st.container(border=True):
        
        st.markdown(
            """
            <div style='display: flex; align-items: center; padding: 10px 16px 16px 16px; border-bottom: 1px solid #5e5c56; margin-bottom: 14px;'>
                <div style='flex: 2.5; text-align: left; font-size: 1.15rem; font-weight: bold; color: var(--text-color);'>Category</div>
                <div style='flex: 2; text-align: center; font-size: 1.15rem; font-weight: bold; color: var(--text-color);'>Planned amount</div>
                <div style='flex: 2; text-align: center; font-size: 1.15rem; font-weight: bold; color: var(--text-color);'>Actual expense</div>
                <div style='flex: 2; text-align: center; font-size: 1.15rem; font-weight: bold; color: var(--text-color);'>Remaining budget</div>
                <div style='flex: 2; text-align: center; font-size: 1.15rem; font-weight: bold; color: var(--text-color);'>Status</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        for cat, amounts in category_summary.items():
            planned = amounts["planned"]
            actual = amounts["actual"]
            remaining = planned - actual

            is_overbudget = remaining < 0

        
            if is_overbudget:
                border_color = "#e56767"
                bg_color = "rgba(229, 103, 103, 0.12)" 
                rem_color = "#e56767"
                status_html = "⚠️ <b>Overspent</b>"
            else:
                border_color = "#5e5c56"
                bg_color = "#363531" 
                rem_color = "#72c472"
                status_html = "✅ <b>Good</b>"

            st.markdown(
                f"""
                <div style="
                    display: flex; 
                    align-items: center; 
                    background-color: {bg_color}; 
                    border: 1px solid {border_color}; 
                    border-radius: 8px; 
                    padding: 12px 16px; 
                    margin-bottom: 10px;
                ">
                    <div style="flex: 2.5; font-size: 1.1rem; font-weight: 600; color: var(--text-color);">{cat}</div>
                    <div style="flex: 2; text-align: center; color: var(--text-color);">₱{planned:,.2f}</div>
                    <div style="flex: 2; text-align: center; color: var(--text-color);">₱{actual:,.2f}</div>
                    <div style="flex: 2; text-align: center; color: {rem_color}; font-weight: bold;">₱{remaining:,.2f}</div>
                    <div style="flex: 2; text-align: center; color: var(--text-color);">{status_html}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_dashboard(selected_month):
    budget_data = data_loader.load_budget_data() or []
    expense_data = data_loader.load_expense_data() or []

    category_summary = build_category_summary(selected_month, budget_data, expense_data)
    total_income, total_planned, total_actual, money_remaining = calculate_financial_metrics(
        selected_month, budget_data, category_summary
    )

    render_financial_summary(total_income, total_planned, total_actual, money_remaining)
    st.divider()
    render_charts_section(category_summary)
    st.divider()
    render_budget_breakdown(category_summary)