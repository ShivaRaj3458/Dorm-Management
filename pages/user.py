import streamlit as st
import project as p


st.set_page_config(page_title="RD-ADMIN", page_icon="✨", initial_sidebar_state="collapsed")

hide_sidebar = """
<style>
/* Hide sidebar completely */
[data-testid="stSidebar"] {display: none;}

/* Hide "Pages" selector that sometimes appears */
section[data-testid="stSidebarNav"] {display: none;}

/* Hide hamburger menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

try:
    conn=p.get_connection()
    cursor=conn.cursor()
except Exception as e:
    print("Error connecting!!")

st.session_state.fin=False
un=st.session_state.get("un","")
query="select namee from register where user_name=%s"
cursor.execute(query,(un,))
result = cursor.fetchone()

query="select room_no from register where user_name=%s"
cursor.execute(query,(un,))
rn = int(cursor.fetchone()[0])

st.title(f"Welcome {result[0]}: ")
col1, col2, col3 = st.columns((1, 1, 1))

with col1:
    if st.button("Complaint"):
        st.session_state.show_complaint = True

with col2:
    if st.button("Order"):
        st.session_state.show_order = True

if st.session_state.get("show_complaint", False):
    options = ["Plumbing Issues", "Electricity Issues", "Request for Cleaner"]
    xx = st.selectbox("Complaint", options, key="complaint_option")
    if st.button("Confirm Complaint"):
        query = "insert into complaints values(%s,%s)"
        cursor.execute(query, (rn, xx))
        conn.commit()
        st.success("Successfully Complained")
        st.session_state.show_complaint = False

if st.session_state.get("show_order", False):
    options = ["Veg", "Non-Veg"]
    xxx = st.selectbox("Order", options, key="complaint_option")
    if st.button("Confirm Order"):
        query = "insert into orders values(%s,%s)"
        cursor.execute(query, (rn, xxx))
        conn.commit()
        st.success("Successfully Order")
        st.session_state.show_order = False
    
with col3:
    sb=st.button("Log Out")
if sb:
    st.switch_page("project.py")

try:
    cursor.close()
    conn.close()    
except Exception as e:
    print("Error connecting!!")


