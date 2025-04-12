import streamlit as st

def run():
    st.title("🛒 Grocery List")

    if "grocery_items" not in st.session_state:
        st.session_state.grocery_items = []

    # --- Add new item ---
    with st.form("add_form", clear_on_submit=True):
        new_item = st.text_input("Add item:")
        submitted = st.form_submit_button("➕ Add")
        if submitted and new_item.strip():
            st.session_state.grocery_items.append({
                "item": new_item.strip(),
                "checked": False
            })

    st.markdown("## 🧾 Your Items")

    # --- Display and manage existing items ---
    updated_items = []
    for i, entry in enumerate(st.session_state.grocery_items):
        col1, col2, col3, col4 = st.columns([0.05, 0.5, 0.3, 0.15])

        # Checkbox to mark complete
        checked = col1.checkbox("", value=entry["checked"], key=f"check_{i}")

        # Editable text input
        edited_text = col2.text_input("Item", value=entry["item"], label_visibility="collapsed", key=f"text_{i}")

        # Save updated item
        updated_items.append({
            "item": edited_text.strip(),
            "checked": checked
        })

        # Remove button
        if col4.button("❌", key=f"remove_{i}"):
            updated_items.pop(i)
            break  # Break to avoid key mismatch after deletion

        st.markdown("---")

    # Update session state with modified list
    st.session_state.grocery_items = updated_items
