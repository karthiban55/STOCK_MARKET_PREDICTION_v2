import yfinance as yf
import pandas as pd

def get_stock_data(ticker_symbol: str, period: str = "1y"):
    """
    Fetches historical stock data for a given ticker symbol.

    Args:
        ticker_symbol (str): The stock ticker (e.g., 'AAPL', 'GOOGL').
        period (str): The time period for the data (e.g., '1d', '5d', '1mo', '1y', 'max').

    Returns:
        pandas.DataFrame: A DataFrame containing the OHLCV data, or None if the ticker is invalid.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period=period)

        if history.empty:
            print(f"No data found for ticker: {ticker_symbol}. It might be delisted or invalid.")
            return None

        # The index is the date, let's reset it to be a column
        history.reset_index(inplace=True)
        # Convert timestamp to just date
        history['Date'] = history['Date'].dt.date

        print(f"Successfully fetched data for {ticker_symbol}")
        return history

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# This part allows us to test the function directly by running this file
if __name__ == "__main__":
    # Example: Fetch 1 year of data for Apple Inc.
    aapl_data = get_stock_data("AAPL", period="1y")

    if aapl_data is not None:
        print("\n--- Last 5 Days of Apple Inc. (AAPL) Data ---")
        # .tail() shows the last 5 rows of the data
        print(aapl_data.tail())