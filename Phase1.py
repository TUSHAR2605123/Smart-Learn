import streamlit as st

# ------------------------- HOME PAGE -------------------------
def home():
    st.set_page_config(page_title="Smart Learn Home", layout="wide")
    
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

    st.markdown('<h1 class="main-title"> 👩‍🎓 Welcome to Smart Learn 📘</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.image("C:\\Users\\Shree\\Downloads\\Smart Learn Logo Design.png", width=600 )
        st.markdown("###### Developed by @pranav_awasare")
    with col2:
        st.write("🌟 This is a platform for students to learn and share knowledge.")
        st.write("🔑 You can **login**, 📝 **register**, 👤 **update your profile**, 📋 **view student lists**, ✍️ **write blogs**, and more.")
        st.write("📌 Use the sidebar to navigate through the application.")
        st.write("🚀 Feel free to explore the features and functionalities of Smart Learn.")
        st.write("📚 **Features:**")
        st.write("- User Authentication (Login/Register)")
        st.write("- Profile Management (View/Update Profile)")
        st.write("- Student List (View All Students)")
        st.write("- Blog Writing (Create/Edit/Delete Blogs)")
        st.write("- Search Functionality (Search Blogs/Students)")
        st.write("📞 For any assistance, please contact support.")
        st.write("🙏 Thank you for using Smart Learn! 🎉")