import streamlit as st
import project as p
import smtplib
import random
from email.mime.text import MIMEText


def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))


def send_otp(rec_mail, otp):
    """Send OTP to user email."""
    try:
        sender_mail = "shivarajgurajala@gmail.com"
        app_password = "xlztkraeluansgby"

        msg = MIMEText(f"Your OTP for verification is {otp}. Do not share it with anyone.")
        msg["Subject"] = "Email Verification"
        msg["From"] = sender_mail
        msg["To"] = rec_mail

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_mail, app_password)
            server.send_message(msg)

        return True
    except Exception as e:
        st.error(f"❌ Email sending failed: {e}")
        return False


st.set_page_config(page_title="RD", page_icon="✨", initial_sidebar_state="collapsed")
st.session_state.fin=False
hide_sidebar = """
<style>
[data-testid="stSidebar"] {display: none;}
section[data-testid="stSidebarNav"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

for key in ["otp_sent", "otp_verified", "registered"]:
    if key not in st.session_state:
        st.session_state[key] = None


try:
    conn = p.get_connection()
    cursor = conn.cursor()
except Exception as e:
    st.error(f"❌ Database Error: {e}")
    st.stop()

cursor.execute("SELECT COUNT(*) FROM register")
room_no = cursor.fetchone()[0]


st.title("✨ Register for Portal Usage")

name = st.text_input("Full Name")
mail = st.text_input("Email Address")
username = st.text_input("Choose a Username")
password = st.text_input("Create Password (max 8 chars)", type="password")

col1, col2 = st.columns([2, 1])
with col1:
    otp_input = st.text_input("Enter OTP (after requesting below)")
with col2:
    if st.button("Send OTP") and mail:
        otp = generate_otp()
        if send_otp(mail, otp):
            st.session_state.otp_sent = otp
            st.info("📩 OTP sent to your email.")

if otp_input and st.session_state.otp_sent:
    if otp_input == st.session_state.otp_sent:
        st.success("✅ Email Verified")
        st.session_state.otp_verified = True
    else:
        st.error("❌ Incorrect OTP")
        st.session_state.otp_verified = False


if st.button("Register"):
    if not name or not mail or not username or not password:
        st.error("⚠️ All fields are required!")
    elif not st.session_state.otp_verified:
        st.error("⚠️ Please verify your email first.")
    elif len(password) > 8:
        st.error("⚠️ Password must be at most 8 characters long.")
    else:
        cursor.execute("SELECT COUNT(*) FROM LogIn WHERE user_name=%s", (username,))
        if cursor.fetchone()[0] > 0:
            st.error("⚠️ Username already taken.")
        else:
            query = "INSERT INTO register VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (username, password, name, mail, room_no))
            conn.commit()
            st.success("🎉 Registered Successfully")
            st.session_state.registered = True

if st.session_state.registered:
    if st.button("Log In"):
        if username == "Admin":
            st.switch_page("pages/admin.py")
        else:
            st.switch_page("pages/user.py")

cursor.close()
conn.close()
