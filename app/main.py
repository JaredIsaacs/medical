import streamlit as st

from pages import login

# run login

x = login.joniFunc()
if x:
    # User is logged in, show the sidebar
    st.markdown(
        """
        <style>
        div[data-testid="stSidebar"] {
            display: block; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    # User is not logged in, hide the sidebar
    st.markdown(
        """
        <style>
        div[data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

if x:
    advisor_page = st.Page("pages/advisor.py", title="Advisor")
    portfolio_page = st.Page("pages/portfolio.py", title="Portfolio")
    companies_page = st.Page("pages/companies.py", title="Companies")
    sign_out = st.Page("pages/logout.py",title='Sign Out')
    pg = st.navigation([advisor_page, portfolio_page, companies_page,])
    pg.run()

