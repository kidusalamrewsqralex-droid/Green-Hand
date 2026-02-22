import streamlit as st
import hashlib
import json
import os
import pandas as pd

# ---------------- CONFIG ----------------
USERS_FILE = "users.json"
ADMIN_USERNAME = "Square"
ADMIN_PASSWORD = "sqrv2718"

st.set_page_config(
    page_title="Login / Signup",
    page_icon="🌱",
    layout="centered"
)

# ---------------- HELPERS ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# ---------------- AUTH LOGIC ----------------
def login(username, password):
    users = load_users()

    # Admin login
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.logged_in = True
        st.session_state.username = ADMIN_USERNAME
        st.session_state.role = "admin"
        return True

    # Normal user login
    if username in users and hash_password(password) == users[username]["password"]:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = "user"

        # Mark this user as last logged in
        for u in users:
            users[u]["last_logged_in"] = (u == username)

        save_users(users)
        return True

    st.error("❌ Invalid username or password / የተጠቃሚ ስም ወይም የይለፍ ቃል ትክክል አይደለም")
    return False

def auto_login():
    users = load_users()
    for username, info in users.items():
        if info.get("last_logged_in", False):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = info.get("role", "user")
            break

def signup(username, password):
    if username == ADMIN_USERNAME:
        st.error("❌ This username is reserved / ይህ የተጠቃሚ ስም ተይዟል")
        return

    users = load_users()

    if username in users:
        st.error("❌ Username already exists / የተጠቃሚ ስሙ አስቀድሞ አለ")
        return

    users[username] = {
        "password": hash_password(password),
        "role": "user",
        "last_logged_in": True
    }

    # Set all other users as not logged in
    for u in users:
        if u != username:
            users[u]["last_logged_in"] = False

    save_users(users)

    st.success("✅ Signup successful! You are now logged in. / መመዝገብ ተሳክቷል! አሁን ገብተዋል።")

    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.role = "user"

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    users = load_users()
    for u in users:
        users[u]["last_logged_in"] = False
    save_users(users)

# ---------------- AUTO LOGIN ----------------
if not st.session_state.logged_in:
    auto_login()

# ---------------- UI ----------------
st.title("🌱 GREEN HAND LOGIN SYSTEM / የግሪን ሃንድ የመግቢያ ስርዓት")

if "redirected" in st.query_params:
    st.warning("🔒 Please log in to access that page. / ይህን ገጽ ለመጠቀም እባክዎ ይግቡ")

if st.session_state.logged_in:

    st.success(
        f"Welcome, {st.session_state.username} 👋 / እንኳን በደህና መጡ, {st.session_state.username} 👋"
    )

    # ---------- ADMIN DASHBOARD ----------
    if st.session_state.role == "admin":
        st.header("🛠 Admin Dashboard / የአስተዳዳሪ መቆጣጠሪያ ገጽ")

        users = load_users()

        if users:
            df = pd.DataFrame([
                {"Username / የተጠቃሚ ስም": u,
                 "Role / ሚና": info["role"]}
                for u, info in users.items()
            ])
            st.dataframe(df)
        else:
            st.write("No users registered yet. / እስካሁን የተመዘገቡ ተጠቃሚዎች የሉም")

    # ---------- USER DASHBOARD ----------
    else:
        st.header("👤 User Dashboard / የተጠቃሚ መቆጣጠሪያ ገጽ")
        st.write("You are logged in as a normal user / እንደ መደበኛ ተጠቃሚ ገብተዋል")

    if st.button("Logout / ይውጡ"):
        logout()

# ---------------- LOGIN / SIGNUP ----------------
else:
    choice = st.radio(
        "Login / Signup / ይግቡ / ይመዝገቡ",
        ["Login / ይግቡ", "Signup / ይመዝገቡ"]
    )

    if choice == "Login / ይግቡ":
        username = st.text_input("Username / የተጠቃሚ ስም")
        password = st.text_input("Password / የይለፍ ቃል", type="password")

        if st.button("Login / ይግቡ"):
            login(username, password)

    else:
        username = st.text_input("Choose a username / የተጠቃሚ ስም ይምረጡ")
        password = st.text_input("Choose a password / የይለፍ ቃል ይምረጡ", type="password")
        confirm = st.text_input("Confirm password / የይለፍ ቃልዎን ያረጋግጡ", type="password")

        if st.button("Sign Up / ይመዝገቡ"):
            if password != confirm:
                st.error("❌ Passwords do not match / የይለፍ ቃል አይመሳሰልም")
            else:
                signup(username, password)