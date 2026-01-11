# agents/data_agent.py
import yfinance as yf
import pandas as pd

class DataAgent:
    # Change the method signature to accept a 'period'
    def run(self, ticker_symbol: str, period: str = "1y") -> pd.DataFrame | None:
        """Fetches historical stock data for a given period."""
        try:
            ticker = yf.Ticker(ticker_symbol)
            # Use the 'period' variable in the yfinance call
            history = ticker.history(period=period)
            if history.empty:
                print(f"No data for {ticker_symbol} (period={period})")
                return None
            history.reset_index(inplace=True)
            # Convert timestamp to date for cleaner JSON
            history['Date'] = pd.to_datetime(history['Date']).dt.date
            return history
        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            return None