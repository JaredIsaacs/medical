import streamlit as st
from app.services import auth as au

st.header('Sign out:')
st.button(label='Sign Out',on_click=au.sign_out,type='primary')