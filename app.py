import streamlit as st
import pandas as pd
import pickle
import os
import sqlite3

from auth import create_user, login_user
from src.recommender import recommend_with_discount
from src.duplicate_detector import find_duplicates_for_product

st.set_page_config(page_title="AI Commerce", layout="wide")

# ---------------------------
# STYLING
# ---------------------------
st.markdown("""
<style>
.navbar {background:#2874f0;color:white;padding:10px;font-size:20px;}
.card {padding:10px;border-radius:10px;background:white;box-shadow:0 2px 8px rgba(0,0,0,0.2);}
.old {text-decoration:line-through;color:gray;}
.new {color:green;font-weight:bold;}
.badge {background:#388e3c;color:white;padding:3px 6px;border-radius:5px;font-size:12px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------------------
# LOAD DATA
# ---------------------------
base_path = os.path.dirname(__file__)
df = pickle.load(open(os.path.join(base_path, "models/data.pkl"), "rb"))

# ---------------------------
# LOGIN
# ---------------------------
def login_page():
    st.markdown("### 🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(u, p):
            st.session_state.logged_in = True
            st.rerun()

    if st.button("Signup"):
        st.session_state.page = "signup"

# ---------------------------
# HOME
# ---------------------------
def home_page():

    st.markdown('<div class="navbar">🛍️ AI Commerce</div>', unsafe_allow_html=True)

    search = st.text_input("Search Product")

    filtered = df[df['product_name'].str.contains(search, case=False, na=False)]
    product = st.selectbox("Select Product", filtered['product_name'] if len(filtered)>0 else df['product_name'])

    discount = st.slider("Discount", 0, 80, 10)

    if st.button("Analyze"):

        results = recommend_with_discount(product, discount)

        st.subheader("✨ Recommendations")

        cols = st.columns(5)

        for i, row in results.iterrows():
            with cols[i % 5]:
                st.image(row['image'])
                st.markdown(f"""
                <div class="card">
                    <h6>{row['product_name'][:40]}</h6>
                    <p class="old">₹ {row['original_price']}</p>
                    <p class="new">₹ {row['discounted_price']}</p>
                    <span class="badge">{discount}% OFF</span>
                </div>
                """, unsafe_allow_html=True)

        st.subheader("🚨 Similar Products")

        dups = find_duplicates_for_product(product)

        for d in dups:
            st.write(d)

# ---------------------------
# MAIN
# ---------------------------
if not st.session_state.logged_in:
    login_page()
else:
    home_page()