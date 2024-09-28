import streamlit as st
advisor_page=st.Page("pages/advisor.py", title="Advisor")
portfolio_page=st.Page("pages/portfolio.py",title="Portfolio")
companies_page=st.Page("pages/companies.py",title="Companies")
pg = st.navigation([advisor_page,portfolio_page,companies_page])
pg.run()