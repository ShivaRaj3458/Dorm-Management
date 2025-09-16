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

st.session_state.fin=False
st.title("Welcome Admin: ")
col1, col2, col3 = st.columns((1, 1, 1))
with col1:
    x=st.button("Check Complaints")
with col2:
    y=st.button("Check Orders")

try:
    conn=p.get_connection()
    cursor=conn.cursor()

    if x:
        query_comp="select * from complaints"
        cursor.execute(query_comp)
        rows=cursor.fetchall()
        col=[desc[0] for desc in cursor.description]
        st.write("### Complaints:")
        data = [dict(zip(col, row)) for row in rows]
        st.table(data)
        clr=st.button("clear")
        if clr:
            query="delete * from complaints"
            cursor.execute(query)
            conn.commit()
            st.success("Cleared")
    
    if y:
        query_comp="select * from orders"
        cursor.execute(query_comp)
        rows=cursor.fetchall()
        col=[desc[0] for desc in cursor.description]
        st.write("### Orders:")
        data = [dict(zip(col, row)) for row in rows]
        st.table(data)
        clr=st.button("clear")
        if clr:
            query="delete * from orders"
            cursor.execute(query)
            conn.commit()
            st.success("Cleared")
    
    with col3:
        sb=st.button("Log Out")
    if sb:
        st.switch_page("project.py")


    cursor.close()
    conn.close()    

except Exception as e:
    print("Error connecting!!")

