import streamlit as st

from utils.style import load_custom_css
st.set_page_config(page_title="🍽️ Recipe App", layout="wide")

load_custom_css()


import streamlit as st

def load_sidebar():
    st.markdown("""
        <style>
        /* Sidebar Title (Targeting the first h1 in the sidebar) */
        .stSidebar > div:nth-child(1) h1 {
            color: #cc2b5e;  /* soft pink color */
            font-family: 'Segoe Script', cursive; /* cute font style */
            font-size: 2em;  /* Larger font size */
            font-weight: bold;
            text-align: center; /* Center align the title */
            margin-bottom: 20px;
            transition: color 0.3s ease; /* Smooth hover transition */
        }

        /* Hover effect for sidebar title */
        .stSidebar > div:nth-child(1) h1:hover {
            color: #ff69b4; /* Darker pink hover effect */
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #ffd6e8;
            border-right: 2px solid #ffb6d9;
        }

        </style>
    """, unsafe_allow_html=True)

load_sidebar()

st.sidebar.title("🌸Navigation🌸")

page = st.sidebar.radio("Go to:", [
    "Recipe Recommender",
    "Meal Planner",
    "Grocery List",
    "Mystery Box Challenge"
])

# Dynamic page loading
if page == "Recipe Recommender":
    from pages import recipe_search
    recipe_search.run()

elif page == "Meal Planner":
    from pages import meal_planner
    meal_planner.run()

elif page == "Grocery List":
    from pages import grocery_list
    grocery_list.run()

elif page == "Mystery Box Challenge":
    from pages import mystery_box
    mystery_box.run()
