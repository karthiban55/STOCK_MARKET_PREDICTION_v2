# agents/sentiment_agent.py
from newsapi import NewsApiClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

class SentimentAgent:
    def __init__(self):
        # IMPORTANT: Replace 'YOUR_API_KEY' with your actual key
        # Better yet, use environment variables for security
        self.newsapi = NewsApiClient(api_key='30383b2edea04192b3392aa8b058d8c1') 
        self.vader = SentimentIntensityAnalyzer()

    def run(self, company_name: str) -> dict:
        """Fetches news and calculates sentiment."""
        try:
            headlines = self.newsapi.get_everything(q=company_name, language='en', sort_by='relevancy', page_size=10)
            
            sentiment_scores = []
            top_headlines = []
            for article in headlines['articles']:
                score = self.vader.polarity_scores(article['title'])['compound']
                sentiment_scores.append(score)
                top_headlines.append({
                    "title": article['title'],
                    "url": article['url']
                })

            avg_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            return {
                "average_sentiment": round(avg_score, 3),
                "headlines": top_headlines
            }
        except Exception as e:
            print(f"Error fetching sentiment: {e}")
            return {
                "average_sentiment": 0,
                "headlines": []
            }