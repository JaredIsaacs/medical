import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import time
from app.services.db import Database
cash = st.session_state['cash']
balance= int(cash['money'])
db = Database()
localid=st.session_state.user_info['localId']
st.write("Your current balance is: $",balance)
popular_tickers = {'Apple Inc.': 'AAPL', 'Microsoft Corporation': 'MSFT', 'Amazon.com Inc.': 'AMZN', 'Alphabet Inc. (Class C)': 'GOOG', 'Alphabet Inc. (Class A)': 'GOOGL', 'Meta Platforms Inc.': 'META', 'Tesla Inc.': 'TSLA', 'NVIDIA Corporation': 'NVDA', 'UnitedHealth Group Incorporated': 'UNH', 'Johnson & Johnson': 'JNJ', 'Exxon Mobil Corporation': 'XOM', 'Visa Inc.': 'V', 'JPMorgan Chase & Co.': 'JPM', 'Procter & Gamble Company': 'PG', 'Chevron Corporation': 'CVX', 'Mastercard Incorporated': 'MA', 'The Home Depot Inc.': 'HD', 'Eli Lilly and Company': 'LLY', 'AbbVie Inc.': 'ABBV', 'Pfizer Inc.': 'PFE', 'Merck & Co. Inc.': 'MRK', 'PepsiCo Inc.': 'PEP', 'The Coca-Cola Company': 'KO', 'Bank of America Corporation': 'BAC', 'Thermo Fisher Scientific Inc.': 'TMO', 'Broadcom Inc.': 'AVGO', 'Costco Wholesale Corporation': 'COST', 'Cisco Systems Inc.': 'CSCO', "McDonald's Corporation": 'MCD', 'Walmart Inc.': 'WMT', 'The Walt Disney Company': 'DIS', 'Danaher Corporation': 'DHR', 'Accenture plc': 'ACN', 'Linde plc': 'LIN', 'NextEra Energy Inc.': 'NEE', 'Verizon Communications Inc.': 'VZ', 'Adobe Inc.': 'ADBE', 'Salesforce Inc.': 'CRM', 'Comcast Corporation': 'CMCSA', 'Nike Inc.': 'NKE', 'Wells Fargo & Company': 'WFC', 'Intel Corporation': 'INTC', 'Texas Instruments Incorporated': 'TXN', "Lowe's Companies Inc.": 'LOW', 'Qualcomm Incorporated': 'QCOM', 'Amgen Inc.': 'AMGN', 'Honeywell International Inc.': 'HON', 'Philip Morris International Inc.': 'PM', 'United Parcel Service Inc.': 'UPS', 'Caterpillar Inc.': 'CAT', 'The Goldman Sachs Group Inc.': 'GS', 'International Business Machines Corporation': 'IBM', 'Raytheon Technologies Corporation': 'RTX', 'Deere & Company': 'DE', 'Morgan Stanley': 'MS', 'General Electric Company': 'GE', 'Intuit Inc.': 'INTU', 'Advanced Micro Devices Inc.': 'AMD', 'Starbucks Corporation': 'SBUX', 'Medtronic plc': 'MDT', 'The Charles Schwab Corporation': 'SCHW', 'BlackRock Inc.': 'BLK', 'AT&T Inc.': 'T', 'The Boeing Company': 'BA', 'ServiceNow Inc.': 'NOW', 'American Express Company': 'AXP', 'S&P Global Inc.': 'SPGI', 'Prologis Inc.': 'PLD', 'Gilead Sciences Inc.': 'GILD', 'Intuitive Surgical Inc.': 'ISRG', 'Automatic Data Processing Inc.': 'ADP', 'TJX Companies Inc.': 'TJX', 'CVS Health Corporation': 'CVS', 'American Tower Corporation': 'AMT', 'Elevance Health Inc.': 'ELV', 'The Cigna Group': 'CI', 'Lockheed Martin Corporation': 'LMT', 'ConocoPhillips': 'COP', 'Marsh McLennan Companies Inc.': 'MMC', 'Bristol-Myers Squibb Company': 'BMY', 'Stryker Corporation': 'SYK', 'Oracle Corporation': 'ORCL', 'PayPal Holdings Inc.': 'PYPL', 'T-Mobile US Inc.': 'TMUS', 'Mondelez International Inc.': 'MDLZ', 'Analog Devices Inc.': 'ADI', 'Netflix Inc.': 'NFLX', 'Abbott Laboratories': 'ABT', 'Duke Energy Corporation': 'DUK', 'The Southern Company': 'SO', 'Chubb Limited': 'CB', 'Northrop Grumman Corporation': 'NOC', 'Zoetis Inc.': 'ZTS', 'Fiserv Inc.': 'FISV', 'Aon plc': 'AON', 'Intercontinental Exchange Inc.': 'ICE', 'The Progressive Corporation': 'PGR', 'CSX Corporation': 'CSX', 'Humana Inc.': 'HUM'}
st.title("Real-time Stock Prices")
selected_ticker = st.selectbox("Tickers", options=popular_tickers.keys())

tricker_symbol=popular_tickers[selected_ticker]
tricker_stock=yf.Ticker(tricker_symbol)
# Create a matplotlib figure
fig, ax = plt.subplots()

# Use st.pyplot to display the plot
plot = st.pyplot(fig)

# Loop to fetch and update stock values
while True:
    # Get the historical prices for Apple stock
    historical_prices = tricker_stock.history(period='1d', interval='1m')
    
    # Get the latest price and time
    latest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    
    # Clear the plot and plot the new data
    ax.clear()
    ax.plot(historical_prices.index, historical_prices['Close'], label='Stock Value')
    ax.set_xlabel('Time')
    ax.set_ylabel('Stock Value')
    ax.set_title('Apple Stock Value')
    ax.legend(loc='upper left')
    ax.tick_params(axis='x', rotation=45)
    
    # Update the plot in the Streamlit app
    plot.pyplot(fig)
    
    # Show the latest stock value in the app
    st.write(f"Latest Price ({latest_time}): {latest_price}")
    st.write("How many stocks would you like to buy:")
    number_of_stocks=st.text_input("How many stocks would you like to buy:", 0)
    balance= round(balance-(int(number_of_stocks)*latest_price), 2)
    st.write("Your current balance is", balance)
    db.update_user(localid, balance)
    # Sleep for 1 minute before fetching new data
    time.sleep(60)

    