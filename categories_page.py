import streamlit as st

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
    st.title("Categories")
    
    init_categories()
    
    st.subheader("Your Categories")
    st.write("Edit the icon or name directly in the list:")

    for i, category in enumerate(st.session_state.categories):
        col1, col2, col3 = st.columns([0.5, 8, 1.5])
        
        updated_icon = col1.text_input(f"Icon_{i}", value=category["icon"], key=f"icon_edit_{i}", label_visibility="collapsed")
        updated_name = col2.text_input(f"Name_{i}", value=category["name"], key=f"name_edit_{i}", label_visibility="collapsed")
        
        st.session_state.categories[i]["icon"] = updated_icon
        st.session_state.categories[i]["name"] = updated_name
        
        delete_clicked = col3.button("Delete", key=f"del_{i}")
        
        if delete_clicked:
            st.session_state.categories.pop(i)
            st.rerun()

    st.write("---")

    expander = st.expander("➕ ADD NEW CATEGORY")
    
    new_icon = expander.text_input("Category Icon", value="🏷️")
    new_cat_name = expander.text_input("New Category Name")
    save_clicked = expander.button("Save Category")
    
    if save_clicked:
        # check if the name isn't blank and doesn't already exist
        name_exists = any(c["name"].lower() == new_cat_name.lower() for c in st.session_state.categories)
        
        if new_cat_name.strip() and not name_exists:
            st.session_state.categories.append({"name": new_cat_name.strip(), "icon": new_icon})
            st.success(f"Added '{new_cat_name}' successfully!")
            st.rerun()
        elif name_exists:
            st.error("This category already exists.")
        else:
            st.error("Category name cannot be empty.")