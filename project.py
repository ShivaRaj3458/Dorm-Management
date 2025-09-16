import streamlit as st
import mysql.connector
st.set_page_config(page_title="RD", page_icon="✨", initial_sidebar_state="collapsed")
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


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="3458",
        database="project"
    )

if "fin" not in st.session_state:
    st.session_state.fin=False 
if "pchk" not in st.session_state:
    st.session_state.pchk=False

if "pusn" not in st.session_state:
    st.session_state.pusn=False 

if st.session_state.fin==False:
    st.title("WELCOME TO RAJ DORMS")
    un = st.text_input("UserName")
    st.session_state.push=True
    try:
        conn=get_connection()
        cursor=conn.cursor()
    except Exception as e:
        st.error(f"❌ Error: {e}")
    chk=True
    if un:
        cursor.execute("SELECT 1 FROM LogIn WHERE user_name=%s", (un,))
        result = cursor.fetchone()
        if not result:
            st.error("Invalid UserName")
            chk=False
        else:
            st.session_state.un=un
            st.session_state.pusn=True
            chk=True
    password=st.text_input("Password",type="password")
    col1, col2, col3 = st.columns((2, 2, 2))
    with col1:
        rbutt=st.button("Register?")
    with col2:
        butt=st.button("LOG IN")
    with col3:
        fbutt=st.button("Forget Password")
    
    if len(un)==0 and len(password)==0 and butt:
        st.error("Invalid Details")
        st.session_state.pusn=False
    if butt and st.session_state.pusn:
        query=("Select pass from LogIn where user_name=%s")
        if un=="Admin":
            cursor.execute(query,(un,))
            x=cursor.fetchone()[0]
            if x==password:
                st.session_state.fin=True
                st.switch_page("pages/admin.py")
            else:
                st.error("Invalid Password")
        else:
            cursor.execute(query,(un,))
            x=cursor.fetchone()[0]
            if x==password:
                st.session_state.fin=True
                st.switch_page("pages/user.py")
            else:
                st.error("Invalid Password")
    
    cursor.close()
    conn.close()
    if rbutt:
        st.session_state.fin=True
        st.switch_page("pages/register.py")
    if (un and chk) and fbutt:
        st.session_state.fin=True
        st.session_state.un = un
        st.switch_page("pages/forgot.py")
    if fbutt:
        st.session_state.fin=True
        st.switch_page("pages/forgot.py")
   
    


# query = st.text_area("Enter SQL query:", "SELECT * FROM users;")

# if st.button("Run Query"):
#     try:
#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(query)

#         if query.strip().lower().startswith("select"):
#             rows = cursor.fetchall()
#             columns = [desc[0] for desc in cursor.description]

#             # Show results in Streamlit (table-like)
#             st.write("### Query Results")
#             st.table([columns] + rows)  # first row = headers
#         else:
#             conn.commit()
#             st.success("✅ Query executed successfully!")

#         cursor.close()
#         conn.close()

#     except Exception as e:
#         st.error(f"❌ Error: {e}")
