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


def generate_metric_card(title, value, text_color="#f0f0f0", border_color="#5e5c56", bg_color="#363531", subtitle=""):
    subtitle_html = f'<span style="font-size: 0.85rem; color: #e56767; font-weight: 600;">{subtitle}</span>' if subtitle else ""
    return (
        f'<div style="background-color: {bg_color}; padding: 1rem; border-radius: 0.5rem; border: 1px solid {border_color}; margin-bottom: 10px;">'
        f'<div style="font-size: 0.85rem; font-weight: 600; color: #f0f0f0; margin-bottom: 0.5rem;">{title}</div>'
        f'<div style="display: flex; align-items: baseline; gap: 0.75rem; flex-wrap: wrap;">'
        f'<span style="font-size: 1.6rem; font-weight: bold; color: {text_color};">₱{value:,.2f}</span>'
        f'{subtitle_html}'
        f'</div>'
        f'</div>'
    )


def render_financial_summary(total_income, total_planned, total_actual, money_remaining):
    col1, col2 = st.columns(2)
    
    rem_color = "#e56767" if money_remaining < 0 else "#72c472"
    rem_icon = "⚠️" if money_remaining < 0 else "🪙"

    inc_border = "#e56767" if total_income == 0 else "#5e5c56"
    inc_bg = "rgba(229, 103, 103, 0.12)" if total_income == 0 else "#363531"
    inc_subtitle = "⚠️ No amount set" if total_income == 0 else ""

    plan_border = "#e56767" if total_planned == 0 else "#5e5c56"
    plan_bg = "rgba(229, 103, 103, 0.12)" if total_planned == 0 else "#363531"
    plan_subtitle = "⚠️ No amount set" if total_planned == 0 else ""

    with col1:
        st.markdown(
            generate_metric_card("💰 TOTAL INCOME", total_income, border_color=inc_border, bg_color=inc_bg, subtitle=inc_subtitle),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            generate_metric_card("📋 PLANNED EXPENSES", total_planned, border_color=plan_border, bg_color=plan_bg, subtitle=plan_subtitle),
            unsafe_allow_html=True
        )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(generate_metric_card("🧾 ACTUAL EXPENSES", total_actual), unsafe_allow_html=True)
    with col4:
        st.markdown(generate_metric_card(f"{rem_icon} MONEY REMAINING", money_remaining, text_color=rem_color), unsafe_allow_html=True)


def render_budget_progress(total_planned, total_actual):
    if total_planned > 0:
        percent = (total_actual / total_planned) * 100
    else:
        percent = 0.0
    
    visual_percent = min(percent, 100)
    bar_color = "#e56767" if percent > 100 else "#72c472"
    
    st.markdown(
        f"""
        <div style="margin-top: 10px; margin-bottom: 15px; padding: 0 5px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-color);">Budget Usage</span>
                <span style="font-size: 0.95rem; font-weight: bold; color: {bar_color};">{percent:.1f}% Used</span>
            </div>
            <div style="width: 100%; background-color: #363531; border-radius: 8px; height: 14px; border: 1px solid #5e5c56;">
                <div style="width: {visual_percent}%; background-color: {bar_color}; height: 100%; border-radius: 7px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_pie_chart(category_summary):
    labels = [c for c, a in category_summary.items() if a["planned"] > 0]
    sizes = [a["planned"] for c, a in category_summary.items() if a["planned"] > 0]

    fig, ax = plt.subplots(figsize=(6.5, 4), facecolor="none")
    ax.set_facecolor("none")

    if sizes:
        colors = ["#ff4b4b", "#ffa15a", "#f6c915", "#72c472", "#29b5e8", "#ab63fa", "#e56767",]
        wedges, texts, autotexts = ax.pie(
            sizes, 
            autopct="%1.1f%%", 
            startangle=90, 
            colors=colors[:len(sizes)], 
            textprops=dict(color="white", fontsize=11)
        )
        ax.axis("equal")
        
        ax.legend(
            wedges, labels, 
            loc="center left", 
            bbox_to_anchor=(1, 0.5),
            facecolor="#363531", 
            edgecolor="#5e5c56", 
            labelcolor="white", 
            fontsize=11
        )
    else:
        ax.text(0.5, 0.5, "No planned data", ha="center", va="center", color="white", fontsize=13)
        ax.axis("off")

    plt.tight_layout()
    return fig


def configure_bar_chart_axes(ax, categories):
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, color="white", fontsize=12, fontweight='bold')
    ax.invert_yaxis()

    ax.xaxis.set_visible(False)
    for spine in ax.spines.values():
        spine.set_visible(False)


def render_actual_over_planned_chart(category_summary):
    plt.style.use("dark_background")
    categories = list(category_summary.keys())
    planned = [category_summary[cat]["planned"] for cat in categories]
    actual = [category_summary[cat]["actual"] for cat in categories]

    fig, ax = plt.subplots(figsize=(6, 5), facecolor="none")
    ax.set_facecolor("none")

    if categories:
        y_pos = list(range(len(categories)))
        height = 0.35
        
        colors = ["#ff4b4b", "#ffa15a", "#f6c915", "#72c472", "#29b5e8", "#ab63fa", "#e56767",]
        bar_colors = [colors[i % len(colors)] for i in range(len(categories))]
        
        y_pos_planned = [y - height/2 for y in y_pos]
        y_pos_actual = [y + height/2 for y in y_pos]
        
        ax.barh(y_pos_planned, planned, height=height, color=bar_colors, label="Planned")
        ax.barh(y_pos_actual, actual, height=height, color=bar_colors, alpha=0.5, edgecolor="white", label="Actual")

        max_val = max([max(planned), max(actual)]) if planned and actual else 0
        padding = max_val * 0.05
        
        for i, (act, plan) in enumerate(zip(actual, planned)):
            ax.text(max(act, plan) + padding, i, f"₱{act:,.1f} / ₱{plan:,.1f}", va='center', color='white', fontsize=12, fontweight='bold')

        configure_bar_chart_axes(ax, categories)
            
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#a3a3a3', label='Planned'),
            Patch(facecolor='#a3a3a3', alpha=0.5, edgecolor='white', label='Actual')
        ]
        
        ax.legend(
            handles=legend_elements, 
            facecolor="#363531", 
            edgecolor="#5e5c56", 
            labelcolor="white", 
            fontsize=12, 
            loc="upper right", 
            bbox_to_anchor=(0.0, -0.05),
            ncol=1
        )
    else:
        ax.text(0.5, 0.5, "No budget and expense data yet.", ha="center", va="center", color="white", fontsize=13)
        ax.axis("off")

    plt.tight_layout()
    return fig


def get_budget_status_details(remaining):
    if remaining < 0:
        return "#e56767", "rgba(229, 103, 103, 0.12)", "#e56767", "⚠️ <b>Overspent</b>"
    return "#5e5c56", "#363531", "#72c472", "✅ <b>Good</b>"


def generate_breakdown_row(cat, planned, actual, remaining):
    border_color, bg_color, rem_color, status_html = get_budget_status_details(remaining)
    return f"""
    <div style="display: flex; align-items: center; background-color: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;">
        <div style="flex: 2.5; font-size: 1.15rem; font-weight: 600; color: var(--text-color);">{cat}</div>
        <div style="flex: 2; text-align: center; font-size: 1.15rem; color: var(--text-color);">₱{planned:,.2f}</div>
        <div style="flex: 2; text-align: center; font-size: 1.15rem; color: var(--text-color);">₱{actual:,.2f}</div>
        <div style="flex: 2; text-align: center; font-size: 1.15rem; color: {rem_color}; font-weight: bold;">₱{remaining:,.2f}</div>
        <div style="flex: 2; text-align: center; font-size: 1.10rem; color: var(--text-color);">{status_html}</div>
    </div>
    """


def render_budget_breakdown(category_summary):
    st.header("Budget Breakdown", text_alignment="center")

    if not category_summary:
        st.info("No budget and expense data yet.")
        return

    with st.container(border=True):
        st.markdown(
            """
            <div style='display: flex; align-items: center; padding: 10px 16px 16px 16px; border-bottom: 1px solid #5e5c56; margin-bottom: 14px;'>
                <div style='flex: 2.5; text-align: left; font-size: 1.25rem; font-weight: bold; color: var(--text-color);'>Category</div>
                <div style='flex: 2; text-align: center; font-size: 1.25rem; font-weight: bold; color: var(--text-color);'>Planned</div>
                <div style='flex: 2; text-align: center; font-size: 1.25rem; font-weight: bold; color: var(--text-color);'>Actual</div>
                <div style='flex: 2; text-align: center; font-size: 1.25rem; font-weight: bold; color: var(--text-color);'>Remaining</div>
                <div style='flex: 2; text-align: center; font-size: 1.25rem; font-weight: bold; color: var(--text-color);'>Status</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        for cat, amounts in category_summary.items():
            planned = amounts["planned"]
            actual = amounts["actual"]
            remaining = planned - actual
            st.markdown(generate_breakdown_row(cat, planned, actual, remaining), unsafe_allow_html=True)


def render_dashboard(selected_month):
    budget_data = data_loader.load_budget_data() or []
    expense_data = data_loader.load_expense_data() or []

    category_summary = build_category_summary(selected_month, budget_data, expense_data)
    total_income, total_planned, total_actual, money_remaining = calculate_financial_metrics(
        selected_month, budget_data, category_summary
    )

    st.header("Budget Analysis", text_alignment="center", divider="rainbow")

    col_metrics, col_pie = st.columns([1.2, 1.0], gap="medium")

    with col_metrics:
        st.header("Budget Summary", text_alignment="center")
        render_financial_summary(total_income, total_planned, total_actual, money_remaining)
        render_budget_progress(total_planned, total_actual)

    with col_pie:
        with st.container(border=True):
            st.markdown("<p style='text-align: center; font-size: 1.15rem; font-weight: bold; margin-bottom: 0px;'>Planned Budget Distribution</p>", unsafe_allow_html=True)
            fig_pie = render_pie_chart(category_summary)
            st.pyplot(fig_pie, use_container_width=True)
            plt.close(fig_pie)

    st.divider()

    col_table, col_graph = st.columns([1.2, 1.0], gap="small")

    with col_table:
        render_budget_breakdown(category_summary)

    with col_graph:
        st.header("Actual Over Planned Expenses", text_alignment="center")
        with st.container(border=True):
            if category_summary:
                fig_barh = render_actual_over_planned_chart(category_summary)
                st.pyplot(fig_barh, use_container_width=True)
                plt.close(fig_barh)
            else:
                st.info("No budget and expense data yet.")

    st.write("---")