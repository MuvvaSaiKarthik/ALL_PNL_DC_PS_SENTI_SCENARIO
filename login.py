import streamlit as st

st.set_page_config(layout='wide')

st.title('ALL PNL DC PS SENTI SCENARIO LOGIN')
# st.sidebar.success('Select a page')


if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

username = st.text_input('Username')
password = st.text_input('Password', type='password')

my_input = username

login = st.button('Login')

if login:
    if username == "VIKABH" and password == "VKB123":
        st.success("Login successful!")
        st.markdown('<span style="color: blue;">Click on home in side menu to see the data</span>', unsafe_allow_html=True)

        st.session_state["my_input"] = my_input

        # st.write("You have entered: ", my_input)

    else:
        st.error("Invalid credentials. Please try again.")


