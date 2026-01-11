// src/components/PredictionCard.jsx
import './PredictionCard.css';
import { formatCurrency } from '../utils/formatCurrency';

const PredictionCard = ({ prediction, sentiment, ticker, currency }) => {
  // --- FIX: Use optional chaining (?.) to prevent crash if sentiment is missing ---
  const sentimentText = sentiment?.label?.charAt(0).toUpperCase() + sentiment?.label?.slice(1) || 'Unavailable';
  const sentimentScore = sentiment?.score?.toFixed(3) || 'N/A';

  const getSentimentClass = () => {
    if (sentiment?.label === 'Positive') return 'positive';
    if (sentiment?.label === 'Negative') return 'negative';
    return 'neutral';
  };

  return (
    <div className="card prediction-card">
      <h3>Analysis for {ticker}</h3>
      <p>
        Predicted Next Close:
        <span>{formatCurrency(prediction, currency)}</span>
      </p>
      <p>
        News Sentiment:
        <span className={getSentimentClass()}>{sentimentText} ({sentimentScore})</span>
      </p>
    </div>
  );
};

export default PredictionCard;