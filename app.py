import streamlit as st
import hashlib

---------------- CONFIG ----------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

st.set_page_config(
page_title="Admin Login",
page_icon="🛠",
layout="centered"
)

---------------- HELPERS ----------------

def hash_password(password):
return hashlib.sha256(password.encode()).hexdigest()

---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
st.session_state.logged_in = False

---------------- AUTH LOGIC ----------------

def login(username, password):
if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
st.session_state.logged_in = True
return True
st.error("❌ Invalid admin credentials")
return False

def logout():
st.session_state.logged_in = False

---------------- UI ----------------

st.title("🛠 ADMIN LOGIN ONLY")

if st.session_state.logged_in:
st.success(f"Welcome, {ADMIN_USERNAME} 👋")

# Admin content here  
st.header("Admin Dashboard")  
st.write("🔒 Only admins can see this content")  

if st.button("Logout"):  
    logout()

else:
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
login(username, password)
ADMIN_PASSWORD_HASH = hash_password("admin123")

def login(username, password):
if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
st.session_state.logged_in = True
return True
st.error("❌ Invalid admin credentials")
return False
if st.session_state.logged_in:
run_admin_dashboard()
else:
st.warning("🔒 You must log in as admin to access this app.")