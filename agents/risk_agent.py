# agents/risk_agent.py
import pandas as pd
import numpy as np
import yfinance as yf

class RiskAgent:
    def run_standard_analysis(self, data: pd.DataFrame) -> dict:
        """Calculates standard and advanced risk metrics."""
        returns = data['Close'].pct_change().dropna()
        
        daily_volatility = returns.std()
        annualized_volatility = daily_volatility * np.sqrt(252)

        market_data = yf.download('^GSPC', start=data['Date'].min(), end=data['Date'].max(), progress=False)
        market_returns = market_data['Close'].pct_change().dropna()
        
        combined = pd.concat([returns, market_returns], axis=1).dropna()
        
        if combined.empty:
            print(f"Warning: No overlapping market data found for the given date range.")
            return {
                "daily_volatility": round(daily_volatility * 100, 2),
                "annualized_volatility": round(annualized_volatility * 100, 2),
                "beta": 0.0,
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0
            }

        combined.columns = ['Stock', 'Market']
        
        covariance = combined.cov().iloc[0, 1]
        market_variance = combined['Market'].var()
        beta = covariance / market_variance if market_variance != 0 else 0

        risk_free_rate = 0.02
        daily_risk_free_rate = (1 + risk_free_rate)**(1/252) - 1
        excess_returns = returns - daily_risk_free_rate
        
        sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() != 0 else 0
        
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = downside_returns.std()
        sortino_ratio = (excess_returns.mean() / downside_std) * np.sqrt(252) if downside_std != 0 else 0

        return {
            "daily_volatility": round(daily_volatility * 100, 2),
            "annualized_volatility": round(annualized_volatility * 100, 2),
            "beta": round(beta, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "sortino_ratio": round(sortino_ratio, 2)
        }

    def run_monte_carlo_simulation(self, data: pd.DataFrame, days=90, simulations=1000) -> dict: # Increased simulations for better intervals
        """Runs a Monte Carlo simulation and calculates confidence intervals."""
        returns = data['Close'].pct_change().dropna()
        last_price = data['Close'].iloc[-1]
        
        avg_daily_return = returns.mean()
        std_dev = returns.std()
        
        simulation_results = np.zeros((days, simulations))
        
        for i in range(simulations):
            prices = [last_price]
            for _ in range(days - 1):
                price_shock = np.random.normal(avg_daily_return, std_dev)
                new_price = prices[-1] * (1 + price_shock)
                prices.append(new_price)
            simulation_results[:, i] = prices
            
        labels = [f"Day {i+1}" for i in range(days)]
        
        # --- NEW: Calculate Confidence Intervals ---
        # For example, 5% and 95% percentiles (90% confidence interval)
        lower_bound_90 = np.percentile(simulation_results, 5, axis=1)
        upper_bound_90 = np.percentile(simulation_results, 95, axis=1)

        # 2.5% and 97.5% percentiles (95% confidence interval)
        lower_bound_95 = np.percentile(simulation_results, 2.5, axis=1)
        upper_bound_95 = np.percentile(simulation_results, 97.5, axis=1)
        
        datasets = []

        # --- Plotting the Confidence Intervals as Fills ---
        datasets.append({
            "label": '95% Confidence Interval',
            "data": upper_bound_95.tolist(),
            "borderColor": 'transparent',
            "backgroundColor": 'rgba(173, 216, 230, 0.1)', # Light blue fill
            "fill": '-1', # Fill to the previous dataset
            "pointRadius": 0,
            "spanGaps": True,
            "order": 1
        })
        datasets.append({
            "label": '95% Confidence Interval (Lower)', # Dummy label, will be filled to previous
            "data": lower_bound_95.tolist(),
            "borderColor": 'transparent',
            "backgroundColor": 'rgba(173, 216, 230, 0.1)',
            "fill": 'start', # Fill from here to the start (upper_bound_95)
            "pointRadius": 0,
            "spanGaps": True,
            "order": 2
        })

        datasets.append({
            "label": '90% Confidence Interval',
            "data": upper_bound_90.tolist(),
            "borderColor": 'transparent',
            "backgroundColor": 'rgba(88, 166, 255, 0.2)', # Darker blue fill
            "fill": '-1',
            "pointRadius": 0,
            "spanGaps": True,
            "order": 3
        })
        datasets.append({
            "label": '90% Confidence Interval (Lower)',
            "data": lower_bound_90.tolist(),
            "borderColor": 'transparent',
            "backgroundColor": 'rgba(88, 166, 255, 0.2)',
            "fill": 'start',
            "pointRadius": 0,
            "spanGaps": True,
            "order": 4
        })

        # --- Highlight the Average Path ---
        average_path = simulation_results.mean(axis=1)
        datasets.append({
            "label": 'Average Expected Path',
            "data": average_path.tolist(),
            "borderColor": '#58a6ff', # A vibrant blue
            "borderWidth": 3,
            "pointRadius": 0,
            "order": 5, # Make sure it's drawn on top
            "fill": False,
        })

        # --- Highlight Best/Worst Case Scenarios (Optional, useful for context) ---
        # Finding the min/max path at the end of the simulation
        final_prices = simulation_results[-1, :]
        best_sim_index = np.argmax(final_prices)
        worst_sim_index = np.argmin(final_prices)

        datasets.append({
            "label": 'Best Case (Simulated)',
            "data": simulation_results[:, best_sim_index].tolist(),
            "borderColor": '#2ecc71', # Green for best case
            "borderWidth": 1,
            "borderDash": [5, 5], # Dashed line
            "pointRadius": 0,
            "order": 6,
            "hidden": True, # Hidden by default, can be toggled in legend
            "fill": False,
        })
        datasets.append({
            "label": 'Worst Case (Simulated)',
            "data": simulation_results[:, worst_sim_index].tolist(),
            "borderColor": '#e74c3c', # Red for worst case
            "borderWidth": 1,
            "borderDash": [5, 5],
            "pointRadius": 0,
            "order": 7,
            "hidden": True, # Hidden by default
            "fill": False,
        })


        return {"labels": labels, "datasets": datasets}