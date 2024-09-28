import streamlit as st
from pages import login

# 2. Perform login check
x = login.joniFunc()

# 3. Conditionally show the sidebar
if x:
    # User is logged in, show the sidebar
    st.markdown(
        """
        <style>
        .stSidebar {
            display: block; 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    advisor_page = st.Page("pages/advisor.py", title="Advisor")
    portfolio_page = st.Page("pages/portfolio.py", title="Portfolio")
    companies_page = st.Page("pages/companies.py", title="Companies")
    sign_out = st.Page("pages/logout.py",title='Sign Out')
    pg = st.navigation([advisor_page, portfolio_page, companies_page,])
    pg.run()
else:
    # User is not logged in, keep the sidebar hidden (already done in step 1)
    st.markdown(
        """
        <style>
        .stSidebar {
            display: none; 
        }
        </style>
        """,
        unsafe_allow_html=True,)
    st.stop()  # Stop execution if not logged in
