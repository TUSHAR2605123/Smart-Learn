import streamlit as st
import mysql.connector 
import hashlib 

# ------------------------- DATABASE CONNECTION -------------------------
def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@pranav1",  # Replace with your actual password
        database="smartlearn"
    )

# ------------------------- PASSWORD HASHING -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------------- LOGIN FORM -------------------------
def login_form():
    st.set_page_config(page_title="Smart Learn Login", layout="wide")

    
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Smart Learn 📘</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔑 Learn Login")
        email=st.text_input("Email")
    with col1:
        password = st.text_input("Password", type='password')

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        connection = create_db_connection()
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password_hash=%s", (email, hashed_password))
        user = cursor.fetchone()
        connection.close()

        if user:
            st.success("✅ Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.user_email = email
        else:
            st.error("❌ Invalid email or password")

# ------------------------- REGISTER FORM -------------------------
def register_form():
    st.set_page_config(page_title="Smart Learn Registration", layout="wide")
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Smart Learn 📘</h1>', unsafe_allow_html=True)
    st.markdown("### 📝 Registration")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
    with col2:
        last_name = st.text_input("Last Name")
        mobile = st.text_input("Mobile Number")

    address = st.text_input("Address")

    col3, col4 = st.columns(2)
    with col3:
        degree = st.text_input("Degree")
        college = st.text_input("College")
    with col4:
        passyear = st.text_input("Passout Year")
        university = st.text_input("University")

    col5, col6 = st.columns(2)
    with col5:
        password = st.text_input("Password", type='password')
    with col6:
        confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Register"):
        if not (first_name and last_name and email and password and confirm_password):
            st.warning("Please fill all required fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        # Check for existing user
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            st.warning("User already exists with this email.")
            connection.close()
            return

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, mobile_number, address, degree, college, passout_year, university, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, mobile, address, degree, college, passyear, university, hashed_password))

        connection.commit()
        cursor.close()
        connection.close()

        st.success("✅ Registered successfully! You can now login.")