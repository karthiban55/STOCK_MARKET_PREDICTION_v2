// src/pages/NewsPage.jsx
import { useState } from 'react';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import NewsList from '../components/NewsList';
import PredictionCard from '../components/PredictionCard'; // We can reuse this to show sentiment

const NewsPage = () => {
  const [ticker, setTicker] = useState('TSLA'); // Default ticker
  const [newsData, setNewsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setNewsData(null);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/news/${ticker}`);
      setNewsData(response.data);
    } catch (err) {
      setError(`Failed to fetch news for ${ticker}.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Helper component to display the sentiment score nicely
  const SentimentDisplay = ({ sentiment }) => {
    const sentimentText = (score) => {
      if (score > 0.05) return 'Positive';
      if (score < -0.05) return 'Negative';
      return 'Neutral';
    };

    return (
      <div className="card">
        <h3>Overall Sentiment for {ticker}</h3>
        <p className="sentiment-score">
          {sentimentText(sentiment.average_sentiment)}
          <span>({sentiment.average_sentiment})</span>
        </p>
      </div>
    );
  };

  return (
    <div className="page-container">
      <h2>News & Sentiment Analysis</h2>
      <p className="page-description">
        Enter a stock ticker to get the latest news headlines and see the overall market sentiment.
      </p>
      <SearchBar ticker={ticker} setTicker={setTicker} onSearch={handleSearch} />

      {loading && <p className="loading">Fetching news...</p>}
      {error && <p className="error">{error}</p>}

      {newsData && (
        <div className="news-results-layout">
          <SentimentDisplay sentiment={newsData.sentiment} />
          <NewsList headlines={newsData.sentiment.headlines} />
        </div>
      )}
    </div>
  );
};

export default NewsPage;