# agents/visualizing_agent.py
import pandas as pd

class VisualizingAgent:
    def run(self, data: pd.DataFrame) -> dict:
        labels = [d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else str(d) for d in data['Date']]
        
        # --- COLOR CHANGE ---
        chart_line_color = "#58a6ff" # Professional Blue

        chart_data = {
            "price_chart": {
                "labels": labels,
                "datasets": [{
                    "label": "Closing Price",
                    "data": data['close'].tolist(),
                    "borderColor": chart_line_color, # Use the new color
                    "borderWidth": 2,
                    "pointRadius": 0,
                    "fill": True,
                    "tension": 0.4
                }]
            }
            # RSI chart data can be added here if needed
        }
        return chart_data