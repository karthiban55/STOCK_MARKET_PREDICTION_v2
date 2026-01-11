// src/components/LivePriceCard.jsx
import './LivePriceCard.css';
import { formatCurrency } from '../utils/formatCurrency'; // Import the helper

const LivePriceCard = ({ liveData }) => {
  const isPositive = liveData.change >= 0;

  return (
    <div className="live-price-card">
      {/* --- THIS LINE IS CHANGED --- */}
      <h1 className="current-price">{formatCurrency(liveData.price, liveData.currency)}</h1>
      <p className={`price-change ${isPositive ? 'positive' : 'negative'}`}>
        {isPositive ? '+' : ''}{liveData.change.toFixed(2)} 
        ({isPositive ? '+' : ''}{liveData.change_percent.toFixed(2)}%) Today
      </p>
    </div>
  );
};
export default LivePriceCard;