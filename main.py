# main.py
import json
import requests
import yfinance as yf
import pandas as pd  # <-- THIS IMPORT IS NEW
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware

# (Import all your agents...)
from agents.data_agent import DataAgent
from agents.technical_agent import TechnicalAgent
from agents.sentiment_agent import SentimentAgent
from agents.prediction_agent import PredictionAgent
from agents.visualizing_agent import VisualizingAgent
from agents.risk_agent import RiskAgent
from agents.comparison_agent import ComparisonAgent
from agents.strategy_agent import StrategyAgent

# (Setup FastAPI app and CORS...)
app = FastAPI(
    title="MarketPulse API",
    description="An API that uses a team of agents to perform stock analysis.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (Instantiate all your agents...)
data_agent = DataAgent()
technical_agent = TechnicalAgent()
sentiment_agent = SentimentAgent()
prediction_agent = PredictionAgent()
visualizing_agent = VisualizingAgent()
risk_agent = RiskAgent()
comparison_agent = ComparisonAgent()
strategy_agent = StrategyAgent()

# (All other endpoints: / , /market/top-stocks , /search , /analyze , etc...)
@app.get("/")
def read_root():
    return {"message": "Welcome to the MarketPulse API!"}
    
@app.get("/market/top-stocks")
def get_top_stocks():
    top_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'RELIANCE.NS', 'TCS.NS']
    results = []
    for ticker_str in top_tickers:
        data = data_agent.run(ticker_str, period="5d")
        if data is not None and not data.empty:
            try:
                info = yf.Ticker(ticker_str).info
                currency = info.get("currency", "USD")
            except Exception:
                currency = "USD"
            latest_price = data['Close'].iloc[-1]
            previous_price = data['Close'].iloc[-2]
            change = latest_price - previous_price
            change_percent = (change / previous_price) * 100
            results.append({
                "ticker": ticker_str, "price": round(latest_price, 2),
                "change": round(change, 2), "change_percent": round(change_percent, 2),
                "currency": currency
            })
    return results

@app.get("/search/{query}")
def search_tickers(query: str = Path(..., min_length=1, max_length=50)):
    ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        matches = data.get("bestMatches", [])
        formatted_results = [{"ticker": match["1. symbol"], "name": match["2. name"]} for match in matches]
        return {"results": formatted_results}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error communicating with financial data provider: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

@app.get("/analyze/{ticker_symbol}")
def analyze_stock(ticker_symbol: str, period: Optional[str] = "1y"):
    raw_data = data_agent.run(ticker_symbol, period=period)
    if raw_data is None:
        raise HTTPException(status_code=404, detail="Could not fetch data for the ticker.")
    enriched_data = technical_agent.run(raw_data.copy())
    prediction = prediction_agent.run(enriched_data.copy()) 
    sentiment = sentiment_agent.run(ticker_symbol)
    chart_data = visualizing_agent.run(enriched_data)
    try:
        info = yf.Ticker(ticker_symbol).info
        currency = info.get("currency", "USD")
    except Exception:
        currency = "USD"
    return {
        "ticker": ticker_symbol, "prediction": round(prediction, 2),
        "sentiment": sentiment, "chart_data": chart_data,
        "currency": currency
    }

@app.get("/live/{ticker_symbol}")
def get_live_data(ticker_symbol: str):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        current_price = info.get("regularMarketPrice", info.get("currentPrice"))
        previous_close = info.get("previousClose")
        currency = info.get("currency", "USD")
        if current_price is None or previous_close is None:
            raise HTTPException(status_code=404, detail=f"Live price data not available for {ticker_symbol}.")
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100
        color = "green" if change >= 0 else "red"
        key_stats = {
            "open": info.get("open"), "dayHigh": info.get("dayHigh"),
            "dayLow": info.get("dayLow"), "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"), "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"), "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "volume": info.get("volume"), "averageVolume": info.get("averageVolume"),
        }
        intraday_data = ticker.history(period="1d", interval="5m")
        if intraday_data.empty:
            raise HTTPException(status_code=404, detail="Could not fetch intraday data.")
        chart_labels = intraday_data.index.strftime('%H:%M').tolist()
        chart_values = intraday_data['Close'].tolist()
        return {
            "ticker": ticker_symbol, "price": round(current_price, 2),
            "change": round(change, 2), "change_percent": round(change_percent, 2),
            "color": color, "currency": currency, "key_stats": key_stats,
            "intraday_chart": {
                "labels": chart_labels,
                "datasets": [{
                    "label": "Price", "data": chart_values, "borderColor": "#58a6ff",
                    "borderWidth": 2, "pointRadius": 0, "fill": True, "tension": 0.4
                }]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch live data: {e}")

@app.get("/risk/{ticker_symbol}")
def get_risk_assessment(ticker_symbol: str):
    raw_data = data_agent.run(ticker_symbol, period="5y")
    if raw_data is None:
        raise HTTPException(status_code=404, detail="Could not fetch data for risk analysis.")
    risk_metrics = risk_agent.run_standard_analysis(raw_data.copy())
    monte_carlo_data = risk_agent.run_monte_carlo_simulation(raw_data.copy())
    return {
        "ticker": ticker_symbol, 
        "risk_metrics": risk_metrics,
        "monte_carlo_chart": monte_carlo_data
    }

@app.get("/news/{ticker_symbol}")
def get_news_and_sentiment(ticker_symbol: str):
    sentiment = sentiment_agent.run(ticker_symbol)
    if not sentiment or not sentiment.get("headlines"):
        raise HTTPException(status_code=404, detail="Could not fetch news for the ticker.")
    return {"ticker": ticker_symbol, "sentiment": sentiment}

@app.get("/compare/")
def get_comparison(tickers: List[str] = Query(..., min_length=2, max_length=4, alias="tickers[]")):
    all_data_frames = {}
    for ticker in tickers:
        data = data_agent.run(ticker)
        if data is not None and not data.empty:
            all_data_frames[ticker] = data
    if not all_data_frames:
        raise HTTPException(status_code=404, detail="Could not fetch data for any of the provided tickers.")
    comparison_chart_data = comparison_agent.run(all_data_frames)
    return comparison_chart_data


# --- NEW: ENDPOINT FOR STRATEGY BACKTESTING ---
@app.get("/strategy/backtest/{ticker_symbol}")
def run_strategy_backtest(
    ticker_symbol: str, 
    strategy: str = Query(..., description="The strategy to run (e.g., 'rsi', 'macd')"),
    period: Optional[str] = "1y"
):
    """
    Runs a backtest for a given stock and strategy.
    """
    print(f"\n--- Strategy Endpoint Started: {ticker_symbol} | {strategy} | {period} ---")
    try:
        # 1. Get data
        print(f"[Main] Calling DataAgent for {ticker_symbol}...")
        raw_data = data_agent.run(ticker_symbol.upper(), period=period)
        if raw_data is None or raw_data.empty:
            print("[Main] DataAgent returned None or Empty.")
            raise HTTPException(status_code=404, detail="Could not fetch data for the ticker.")
        print(f"[Main] DataAgent OK. Got {len(raw_data)} rows.")

        # 2. Add technical indicators
        print("[Main] Calling TechnicalAgent...")
        technical_data = technical_agent.run(raw_data.copy())
        if technical_data.empty:
            print("[Main] TechnicalAgent returned Empty data (not enough data for indicators).")
            raise HTTPException(status_code=400, detail="Not enough data to calculate technical indicators.")
        print(f"[Main] TechnicalAgent OK. Data has {len(technical_data)} rows after dropna.")
        
        # 3. Run the selected strategy
        print(f"[Main] Calling StrategyAgent with '{strategy}' strategy...")
        results = strategy_agent.run(strategy_name=strategy, data=technical_data)
        print("[Main] StrategyAgent OK.")
        
        # 4. Also return the price data for the chart
        print("[Main] Formatting price data for chart...")
        price_data_df = technical_data.reset_index()
        
        # Find the date column
        date_col_name = price_data_df.columns[0] # Usually 'Date' or 'index'
        print(f"[Main] Using date column: '{date_col_name}'")

        # --- START FIX ---
        # Create a copy to avoid SettingWithCopyWarning
        price_data = price_data_df[[date_col_name, 'Close']].copy()
        
        # **THIS IS THE FIX:** Explicitly convert the column to datetime
        price_data[date_col_name] = pd.to_datetime(price_data[date_col_name])
        
        # Now we can safely format it
        price_data[date_col_name] = price_data[date_col_name].dt.strftime('%Y-%m-%d')
        
        # Rename the column to 'Date' for the frontend
        price_data.rename(columns={date_col_name: 'Date'}, inplace=True)
        # --- END FIX ---
        
        print("[Main] Strategy Endpoint Complete.")
        return {
            "backtest_results": results,
            "price_data": price_data.to_dict('records') 
        }
        
    except Exception as e:
        # --- THIS WILL CATCH THE CRASH ---
        print(f"!!! CRASH IN /strategy/backtest ENDPOINT !!!")
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc() # This will print the FULL traceback
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")