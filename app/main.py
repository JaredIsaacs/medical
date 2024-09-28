from datetime import datetime, timedelta
import time
import streamlit as st
import yfinance as yf
import pandas as pd
import schedule

popular_tickers = [
    "AAPL", "MSFT", "AMZN", "GOOG", "GOOGL", "META", "TSLA", "NVDA", "BRK.B", "UNH", 
    "JNJ", "XOM", "V", "JPM", "PG", "CVX", "MA", "HD", "LLY", "ABBV", 
    "PFE", "MRK", "PEP", "KO", "BAC", "TMO", "AVGO", "COST", "CSCO", "MCD", 
    "WMT", "DIS", "DHR", "ACN", "LIN", "NEE", "VZ", "ADBE", "CRM", "CMCSA", 
    "NKE", "WFC", "INTC", "TXN", "LOW", "QCOM", "AMGN", "HON", "PM", "UPS", 
    "CAT", "GS", "IBM", "RTX", "DE", "MS", "GE", "INTU", "AMD", "SBUX", 
    "MDT", "SCHW", "BLK", "T", "BA", "NOW", "AXP", "SPGI", "PLD", "GILD", 
    "ISRG", "ADP", "TJX", "CVS", "AMT", "ELV", "CI", "LMT", "COP", "MMC", 
    "BMY", "SYK", "ORCL", "PYPL", "TMUS", "MDLZ", "ADI", "NFLX", "ABT", "DUK", 
    "SO", "CB", "NOC", "ZTS", "FISV", "AON", "ICE", "PGR", "CSX", "HUM"
]

logtxtbox = st.empty()

rolling_window = pd.DataFrame()
daily_high = float('-inf')
daily_low = float('inf')
buying_momentum = 0
selling_momentum = 0

selected_ticker = st.selectbox("Tickers", popular_tickers)

stock = yf.Ticker(selected_ticker)
data = stock.history(period="1d", interval="1m")

def process_stock_update():
  global rolling_window, data
  global daily_high, daily_low, buying_momentum, selling_momentum

  if not data.empty:
    update = data.iloc[0].to_frame().T
    time_str = update.index[0].time()
    logtxtbox.caption(time_str)

    rolling_window = pd.concat([rolling_window, update], ignore_index=False)

    daily_high = max(daily_high, update['Close'].values[0])
    daily_low = min(daily_low, update['Close'].values[0])

    if len(rolling_window) >= 2:
      price_change = update['Close'].values[0] - rolling_window['Close'].iloc[-2]
      if price_change > 0:
        buying_momentum += price_change
      else:
        selling_momentum += abs(price_change)

    if len(rolling_window) > 5:
      rolling_window = rolling_window.iloc[1:]

    calculate_insights(rolling_window)

def get_market_open_duration(window):
  current_time = window.index[-1].time()

  previous_trading_day = datetime.today() - timedelta(days=1)

  current_datetime = datetime.combine(previous_trading_day, current_time)

  market_start_time = datetime.combine(previous_trading_day, datetime.strptime("09:30:00", "%H:%M:%S").time())

  market_open_duration = (current_datetime - market_start_time).total_seconds() / 60

  return market_open_duration

#Function to calculate insights like moving averages and trends
def calculate_insights(window):
    if len(window) >= 5:
        # Calculate 5-minute rolling average of the 'Close' prices
        rolling_avg = window['Close'].rolling(window=5).mean().iloc[-1]

        # Calculate price change and volume change
        price_change = window['Close'].iloc[-1] - window['Close'].iloc[-2] if len(window) >= 2 else 0
        volume_change = window['Volume'].iloc[-1] - window['Volume'].iloc[-2] if len(window) >= 2 else 0

    
        # Calculate Exponential Moving Average (EMA) and Bollinger Bands (with a 5-period window)
        ema = window['Close'].ewm(span=5, adjust=False).mean().iloc[-1]
        std = window['Close'].rolling(window=5).std().iloc[-1]
        bollinger_upper = rolling_avg + (2 * std)
        bollinger_lower = rolling_avg - (2 * std)

        # Calculate Relative Strength Index (RSI) if there are enough periods (14 is typical)
        delta = window['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14, min_periods=1).mean().iloc[-1]
        avg_loss = loss.rolling(window=14, min_periods=1).mean().iloc[-1]
        rs = avg_gain / avg_loss if avg_loss != 0 else float('nan')
        rsi = 100 - (100 / (1 + rs))
        
        market_open_duration = get_market_open_duration(window)

        # Print the calculated insights
        print(f"5-minute Rolling Average: {rolling_avg:.2f}")
        print(f"EMA: {ema:.2f}")
        print(f"RSI: {rsi:.2f}")
        print(f"Bollinger Upper Band: {bollinger_upper:.2f}, Lower Band: {bollinger_lower:.2f}")
        print(f"Price Change: {price_change:.2f}")
        print(f"Volume Change: {volume_change}")
        print(f"Daily High: {daily_high:.2f}, Daily Low: {daily_low:.2f}")
        print(f"Buying Momentum: {buying_momentum:.2f}, Selling Momentum: {selling_momentum:.2f}")
        print(f"Market has been open for {market_open_duration:.2f} minutes")
        
        #if int(market_open_duration) % 5 == 0:  # Trigger LLM every 5 minutes
        #    get_natural_language_insights(
        #        rolling_avg, ema, rsi, bollinger_upper, bollinger_lower,
        #        price_change, volume_change, market_open_duration, daily_high, daily_low, buying_momentum, selling_momentum, window.index[-1].time().strftime("%H:%M:%S")
        #    )


# Use st.empty to create a placeholder for the dataframe
placeholder = st.empty()

while True:
    process_stock_update()
    with placeholder.container():  # Use a container for better visual updates
        st.dataframe(rolling_window)
    time.sleep(60)
