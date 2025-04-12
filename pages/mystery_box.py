import streamlit as st
import random

def run():
    st.title("🎲 Mystery Box Cooking Challenge")

    ingredients_pool = ["tomato", "cheese", "eggplant", "rice", "chicken", "spinach", "onion", "bell pepper"]
    selected = random.sample(ingredients_pool, 3)

    st.subheader("Your Ingredients:")
    st.write(", ".join(selected))
    st.info("Try finding a creative recipe using only these!")
