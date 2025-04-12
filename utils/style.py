import streamlit as st
def load_custom_css():
    st.markdown("""
        <style>
        /* Background */
        .stApp {
            background-color: #ffe6f0; /* soft pastel pink */
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #ffd6e8;
            border-right: 2px solid #ffb6d9;
        }

        .css-1v0mbdj:hover {
            color: #ff69b4; /* Hover color */
            transform: scale(1.1); /* Slight zoom effect on hover */
        }

        /* Header title */
        .css-10trblm, .stTitle {
            color: #cc2b5e;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            transition: color 0.3s ease; /* Smooth transition for hover */
        }

        .stTitle:hover {
            color: #ff69b4; /* Pink hover color */
        }

        /* Text inputs & buttons */
        input, textarea {
            border: 2px solid #ffb6d9 !important;
            background-color: #fff0f5 !important;
            color: black !important;
        }

        button {
            border-radius: 8px !important;
            background-color: #ffb6d9 !important;
            color: white !important;
            transition: background-color 0.3s ease; /* Smooth button hover */
        }

        button:hover {
            background-color: #ff69b4 !important; /* Darker pink for button hover */
        }

        /* Checkbox color */
        input[type="checkbox"] {
            accent-color: #ff69b4 !important;
        }

        /* Titles and paragraphs */
        h1, h2, h3, p, span {
            color: black !important;
            font-family: 'Segoe Script', cursive;
            transition: color 0.3s ease; /* Smooth transition for hover */
        }

        h1:hover, h2:hover, h3:hover {
            color: #ff69b4; /* Pink hover color for titles */
        }

        p:hover, span:hover {
            color: #ff2a8e; /* Darker pink for text hover */
        }

        /* Sidebar text */
        .css-1v0mbdj {
            color: black !important;
            transition: color 0.3s ease;
        }

        .css-1v0mbdj:hover {
            color: #ff69b4 !important; /* Pink hover color for sidebar items */
        }

        /* Footer text */
        footer {
            color: black !important;
            transition: color 0.3s ease;
        }

        footer:hover {
            color: #ff69b4 !important; /* Pink hover for footer text */
        }

        /* Text in input boxes and text areas */
        input[type='text'], textarea {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

