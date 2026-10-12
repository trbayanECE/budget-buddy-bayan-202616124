import streamlit as st
import matplotlib.pyplot as plt
import data_loader

def build_category_summary(selected_month, budget_entries, expense_entries):
    summary = {}
    
    for bud in budget_entries:
        if bud["month"] == selected_month:
            cat = bud["category"]
            if cat not in summary:
                summary[cat] = {"planned": 0.0, "actual": 0.0}
            summary[cat]["planned"] += bud["planned_amount"]
            
    for exp in expense_entries:
        if exp["month"] == selected_month:
            cat = exp["category"]
            if cat not in summary:
                summary[cat] = {"planned": 0.0, "actual": 0.0}
            summary[cat]["actual"] += float(exp["amount"])
            
    return summary

# matplotlib piechart: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
def render_pie_chart(category_summary):
    plt.style.use('dark_background')
    
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
        
        ax.pie(sizes, 
               explode=explode, 
               labels=labels, 
               autopct='%1.1f%%', 
               shadow=True, 
               startangle=90)
               
        ax.axis('equal') 
    else:
        ax.text(0.5, 0.5, 'No planned budget data', horizontalalignment='center', verticalalignment='center')
        ax.axis('off')
        
    return fig

# matplotlib bargraph: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
def render_comparison_chart(category_summary):
    plt.style.use('dark_background')
    
    categories = list(category_summary.keys())
    planned = [category_summary[cat]["planned"] for cat in categories]
    actual = [category_summary[cat]["actual"] for cat in categories]
    
    x = range(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    ax.bar([i - width/2 for i in x], planned, width, label='Planned', color='#00d4ff')
    ax.bar([i + width/2 for i in x], actual, width, label='Actual', color='#ff6666')
    
    ax.set_ylabel('Amount (₱)')
    ax.set_title('Planned vs Actual Spending')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    
    legend = ax.legend()
    legend.get_frame().set_alpha(0.0)
    
    plt.tight_layout()
    return fig

def render_budget_breakdown(category_summary):
    st.subheader("Budget Breakdown")
    
    header_col1, header_col2, header_col3, header_col4 = st.columns(4)
    header_col1.markdown("**Category**")
    header_col2.markdown("**Planned**")
    header_col3.markdown("**Actual**")
    header_col4.markdown("**Status**")
    
    st.markdown("---")
    
    for cat, amounts in category_summary.items():
        row_col1, row_col2, row_col3, row_col4 = st.columns(4)
        
        row_col1.write(cat)
        row_col2.write(f"₱{amounts['planned']:,.2f}")
        row_col3.write(f"₱{amounts['actual']:,.2f}")
        
        diff = amounts['planned'] - amounts['actual']
        
        if diff < 0:
            row_col4.error(f"Over budget by ₱{abs(diff):,.2f}")
        else:
            row_col4.success(f"₱{diff:,.2f} remaining")

def render_dashboard(selected_month):
    st.header("Financial Dashboard")
    
    budget_data = data_loader.load_budget_data()
    expense_data = data_loader.load_expense_data()
    
    if not budget_data and not expense_data:
        st.info("No data found. Add budgets or expenses first.")
        return
        
    months = []
    for entry in budget_data + expense_data:
        if entry["month"] not in months:
            months.append(entry["month"])
            
    summary = build_category_summary(selected_month, budget_data, expense_data)
    
    st.markdown("---")
    st.subheader("Budget Distribution", text_alignment="center")
    st.pyplot(render_pie_chart(summary))
    
    st.markdown("---")
    st.subheader("Spending Comparison", text_alignment="center")
    st.pyplot(render_comparison_chart(summary))

    st.markdown("---")
    render_budget_breakdown(summary)

# problem 1: how to make graphs dark mode