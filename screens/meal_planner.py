import streamlit as st

def run():
    st.title("📅 Weekly Meal Planner")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if "meal_plan" not in st.session_state:
        st.session_state.meal_plan = {}

    for day in days:
        meal = st.text_input(f"{day}'s Meal", value=st.session_state.meal_plan.get(day, ""))
        st.session_state.meal_plan[day] = meal

    st.markdown("---")
    if st.button("🛒 Generate Grocery List"):
        st.write("🚧 Coming soon: auto-combined ingredients from above meals.")
