import streamlit as st
import project as p
import random
import smtplib
from email.mime.text import MIMEText


def generate_otp():
    return str(random.randint(100000,999999))

def send_otp(rec_mail, otp):
    try:
        sender_mail="shivarajgurajala@gmail.com"
        app_password="xlztkraeluansgby"
        
        msg=MIMEText(f"Your OTP for verification is {otp}. Do not share it with others.")
        msg["Subject"]="Mail Verification"
        msg["From"]=sender_mail
        msg["To"]=rec_mail
        
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login(sender_mail,app_password)
            server.send_message(msg)
            return True
    except:
        st.error("Enter Valid Email!!")
        return False


st.set_page_config(page_title="RD forgot", page_icon="✨", initial_sidebar_state="collapsed")

hide_sidebar = """
<style>
[data-testid="stSidebar"] {display: none;}
section[data-testid="stSidebarNav"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

st.session_state.fin=False

if "otp" not in st.session_state:
    st.session_state.otp = None
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "verified" not in st.session_state:
    st.session_state.verified = False
if "cf" not in st.session_state:
    st.session_state.cf = False

try:
    conn = p.get_connection()
    cursor = conn.cursor()
except Exception as e:
    st.error(f"❌ Error: {e}")

un = st.text_input("User Name", st.session_state.get("un", ""))
x = ""

if un:
    query = "select mail from register where user_name=%s"
    cursor.execute(query, (un,))
    result = cursor.fetchone()
    if result:
        x = result[0]
        st.write(f"Mail ID: {x}")

if st.button("Send Otp"):
    if not un:
        st.warning("Enter UserName")
    elif x:
        otp = generate_otp()
        if send_otp(x, otp):
            st.success("OTP sent successfully!")
            st.session_state.otp = otp
            st.session_state.otp_sent = True

if st.session_state.otp_sent and not st.session_state.verified:
    otpp = st.text_input("Enter OTP", key="otp_input")
    if st.button("Verify"):
        if otpp and otpp == st.session_state.otp:
            st.success("✅ Verified")
            st.session_state.verified = True
        else:
            st.error("❌ Wrong OTP!!")


if st.session_state.verified:
    npw = st.text_input("New Password", type="password", key="new_pw")
    cf=st.button("Confirm")
    if cf and npw and len(npw)<=8:
        query="update register set pass=%s where user_name=%s"
        cursor.execute(query,(npw,un,))
        conn.commit()
        st.success("Password change success!")
        st.session_state.cf=True
    if len(npw)>8:
        st.error("Password Size Exceeded!")

if st.session_state.cf:
    Li=st.button("LogIn")
    if Li and un=="Admin":
        st.switch_page("pages/admin.py")
    if Li and un:
        st.switch_page("pages/user.py")
cursor.close()
conn.close()
