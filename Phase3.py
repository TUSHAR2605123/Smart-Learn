import streamlit as st
import mysql.connector 
import hashlib 
import pandas as pd
import os

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

# Student List Show from database
def student_list():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT first_name, last_name, email, mobile_number FROM users")
    students = cursor.fetchall()
    cursor.close()
    connection.close()

    if students:
        df = pd.DataFrame(students, columns=["First Name", "Last Name", "Email", "Mobile Number"],index=range(1, len(students)+1))
        st.write("### 👥 Student List")
        st.dataframe(df)
    else:
        st.write("No students found.")

def profile():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email, mobile_number, address, degree, college, passout_year, university FROM users WHERE email=%s", (st.session_state.user_email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            st.markdown("### 👤 My Profile")
            st.write("Welcome! Here are your profile details:")
            st.write(f"**First Name:** {user[0]}")
            st.write(f"**Last Name:** {user[1]}")
            st.write(f"**Email:** {user[2]}")
            st.write(f"**Mobile Number:** {user[3]}")
            st.write(f"**Address:** {user[4]}")
            st.write(f"**Degree:** {user[5]}")
            st.write(f"**College:** {user[6]}")
            st.write(f"**Passout Year:** {user[7]}")
            st.write(f"**University:** {user[8]}")
            if st.button("Edit Profile"):
                st.session_state["edit_mode"] = True
        else:
            st.error("User not found.")
    else:
        st.warning("### 🚪 Please login to view your profile.")

def edit_profile():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email, mobile_number, address, degree, college, passout_year, university FROM users WHERE email=%s", (st.session_state.user_email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            st.markdown("### ✏️ Edit Profile")
            first_name = st.text_input("First Name", value=user[0])
            last_name = st.text_input("Last Name", value=user[1])
            email = st.text_input("Email", value=user[2])
            mobile = st.text_input("Mobile Number", value=user[3])
            address = st.text_area("Address", value=user[4])
            degree = st.text_input("Degree", value=user[5])
            college = st.text_input("College", value=user[6])
            passyear = st.text_input("Passout Year", value=user[7])
            university = st.text_input("University", value=user[8])

            if st.button("Save Changes"):
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users SET first_name=%s, last_name=%s, email=%s, mobile_number=%s, address=%s, degree=%s, college=%s, passout_year=%s, university=%s
                    WHERE email=%s
                """, (first_name, last_name, email, mobile, address, degree, college, passyear, university, st.session_state.user_email))
                connection.commit()
                cursor.close()
                connection.close()

                st.success("Profile updated successfully!")
                st.session_state["edit_mode"] = False
        else:
            st.error("User not found.")
    else:
        st.warning("### 🚪 Please login to edit your profile.")

# File to save posts
DATA_FILE = "student_wall.csv"

def load_posts():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["username", "content", "image", "time"])