import pandas as pd
from finta import TA

class TechnicalAgent:
    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """Adds technical indicators to the dataframe using finta."""

        # --- 1. IMPORTANT: finta requires lowercase column names ---
        # We rename the columns from yfinance (e.g., "Open") to finta's format ("open")
        data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)

        # --- 2. Use the correct finta syntax: TA.INDICATOR(data) ---
        
        # TA.RSI() returns a single Series, so we assign it to a new column
        data['RSI'] = TA.RSI(data)
        
        # TA.MACD() returns a DataFrame with 3 columns, so we join it
        macd_data = TA.MACD(data)
        data = pd.concat([data, macd_data], axis=1)

        # --- 3. Drop rows with NaN values ---
        data.dropna(inplace=True)
        return data