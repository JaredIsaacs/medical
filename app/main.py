import streamlit as st

advisor_page=st.Page("pages/advisor.py", title="Advisor", icon=":material/person:")
portfolio_page=st.Page("pages/portfolio.py", title="Portfolio", icon=":material/account_balance:")
companies_page=st.Page("pages/companies.py", title="Companies", icon=":material/add_to_queue:")

pg = st.navigation([advisor_page,portfolio_page,companies_page])
pg.run()