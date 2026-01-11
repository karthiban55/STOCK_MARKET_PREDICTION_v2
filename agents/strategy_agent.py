# agents/strategy_agent.py
import pandas as pd
import numpy as np

class StrategyAgent:
    """
    Runs different backtesting strategies on data.
    Assumes the data has already been processed by TechnicalAgent.
    """

    def run_rsi_strategy(self, data: pd.DataFrame, initial_capital=100000.0):
        print("[StrategyAgent] Starting run_rsi_strategy...")
        signals = []
        position = False
        capital = initial_capital
        shares = 0
        
        if data.empty:
            print("[StrategyAgent] Data is empty. Returning default.")
            return {
                "signals": [],
                "metrics": {
                    "strategy_name": "RSI (30/70)", "initial_capital": initial_capital,
                    "final_value": initial_capital, "total_return_pct": 0.0
                }
            }
        
        print(f"[StrategyAgent] Data has {len(data)} rows. Iterating...")
        try:
            for i in range(len(data)):
                row = data.iloc[i]
                
                # --- Error Check 1: Check for valid row data ---
                if 'RSI_14' not in row or 'Close' not in row:
                    raise KeyError(f"Missing 'RSI_14' or 'Close' in data row {i}")
                
                rsi = row['RSI_14']
                close_price = row['Close']
                
                # --- Error Check 2: Check for valid date ---
                date_str = pd.to_datetime(row.name).strftime('%Y-%m-%d')
                
                # --- Buy Signal ---
                if rsi < 30 and not position:
                    shares = capital / close_price
                    capital = 0
                    position = True
                    signals.append({"date": date_str, "type": "BUY", "price": close_price})
                    
                # --- Sell Signal ---
                elif rsi > 70 and position:
                    capital = shares * close_price
                    shares = 0
                    position = False
                    signals.append({"date": date_str, "type": "SELL", "price": close_price})

        except Exception as e:
            # --- THIS WILL CATCH THE CRASH ---
            print(f"!!! CRASH INSIDE RSI LOOP AT ROW {i} !!!")
            print(f"ERROR: {e}")
            print(f"DATA ROW: {row}")
            raise e # Re-raise the exception to send 500 error
                
        print("[StrategyAgent] Loop finished. Calculating final value...")
        final_value = capital + (shares * data.iloc[-1]['Close'])
        total_return = (final_value - initial_capital) / initial_capital * 100
        
        print("[StrategyAgent] RSI Strategy complete.")
        return {
            "signals": signals,
            "metrics": {
                "strategy_name": "RSI (30/70)", "initial_capital": initial_capital,
                "final_value": round(final_value, 2), "total_return_pct": round(total_return, 2)
            }
        }

    # (The MACD function is unchanged, but you can add similar checks)
    def run_macd_strategy(self, data: pd.DataFrame, initial_capital=100000.0):
        print("[StrategyAgent] Starting run_macd_strategy...")
        signals = []
        position = False
        capital = initial_capital
        shares = 0

        if data.empty:
            print("[StrategyAgent] Data is empty. Returning default.")
            return {
                "signals": [],
                "metrics": {
                    "strategy_name": "MACD Crossover", "initial_capital": initial_capital,
                    "final_value": initial_capital, "total_return_pct": 0.0
                }
            }
        
        print(f"[StrategyAgent] Data has {len(data)} rows. Iterating...")
        try:
            for i in range(1, len(data)):
                prev = data.iloc[i-1]
                curr = data.iloc[i]
                
                date_str = pd.to_datetime(curr.name).strftime('%Y-%m-%d')
                
                if (prev['MACD_12_26_9'] < prev['MACDs_12_26_9']) and \
                   (curr['MACD_12_26_9'] > curr['MACDs_12_26_9']) and not position:
                    
                    shares = capital / curr['Close']
                    capital = 0
                    position = True
                    signals.append({"date": date_str, "type": "BUY", "price": curr['Close']})

                elif (prev['MACD_12_26_9'] > prev['MACDs_12_26_9']) and \
                     (curr['MACD_12_26_9'] < curr['MACDs_12_26_9']) and position:
                    
                    capital = shares * curr['Close']
                    shares = 0
                    position = False
                    signals.append({"date": date_str, "type": "SELL", "price": curr['Close']})
        
        except Exception as e:
            # --- THIS WILL CATCH THE CRASH ---
            print(f"!!! CRASH INSIDE MACD LOOP AT ROW {i} !!!")
            print(f"ERROR: {e}")
            print(f"CURRENT ROW: {curr}")
            print(f"PREVIOUS ROW: {prev}")
            raise e

        final_value = capital + (shares * data.iloc[-1]['Close'])
        total_return = (final_value - initial_capital) / initial_capital * 100
        
        print("[StrategyAgent] MACD Strategy complete.")
        return {
            "signals": signals,
            "metrics": {
                "strategy_name": "MACD Crossover", "initial_capital": initial_capital,
                "final_value": round(final_value, 2), "total_return_pct": round(total_return, 2)
            }
        }

    def run(self, strategy_name: str, data: pd.DataFrame):
        """
        Main entry point to run a selected strategy.
        """
        if strategy_name == "rsi":
            return self.run_rsi_strategy(data)
        elif strategy_name == "macd":
            return self.run_macd_strategy(data)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")