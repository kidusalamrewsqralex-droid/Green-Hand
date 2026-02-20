import streamlit as st
import hashlib

# ---------------- CONFIG ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

st.set_page_config(
    page_title="Admin Login",
    page_icon="🛠",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- HELPERS ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
        st.session_state.logged_in = True
        return True
    st.error("❌ Invalid admin credentials")
    return False

def logout():
    st.session_state.logged_in = False

# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard():
    st.success(f"Welcome, {ADMIN_USERNAME} 👋")
    st.header("Admin Dashboard")
    st.write("🔒 Only admins can see this content")
    # Add your admin content here
    if st.button("Logout"):
        logout()

# ---------------- UI ----------------
st.title("🛠 ADMIN LOGIN ONLY")

if st.session_state.logged_in:
    admin_dashboard()
else:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)
    st.warning("🔒 You must log in as admin to access this app.")