# agents/comparison_agent.py
import pandas as pd

class ComparisonAgent:
    def run(self, data_frames: dict) -> dict:
        """
        Normalizes stock prices to compare performance over time.

        Args:
            data_frames (dict): A dictionary where keys are tickers and values are their dataframes.

        Returns:
            A dictionary formatted for Chart.js to draw a multi-line chart.
        """
        performance_data = {}
        labels = []

        for ticker, df in data_frames.items():
            # Normalize the closing price to show percentage growth
            normalized_close = (df['Close'] / df['Close'].iloc[0] - 1) * 100
            performance_data[ticker] = normalized_close.tolist()
            if not labels: # Get labels from the first dataframe
                labels = [d.strftime('%Y-%m-%d') for d in df['Date']]
        
        # Create a list of datasets for Chart.js
        datasets = []
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f'] # Add more colors if needed
        for i, (ticker, data) in enumerate(performance_data.items()):
            datasets.append({
                "label": f"{ticker} Performance (%)",
                "data": data,
                "borderColor": colors[i % len(colors)],
                "fill": False,
                "tension": 0.1
            })

        return {"labels": labels, "datasets": datasets}