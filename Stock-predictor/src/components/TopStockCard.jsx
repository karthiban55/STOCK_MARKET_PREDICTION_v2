// src/components/TopStockCard.jsx
import './TopStockCard.css';
import { formatCurrency } from '../utils/formatCurrency'; // Import the helper

const TopStockCard = ({ stock }) => {
  const isPositive = stock.change >= 0;

  return (
    <div className="stock-card">
      <div className="stock-info">
        <span className="stock-ticker">{stock.ticker}</span>
        {/* --- THIS LINE IS CHANGED --- */}
        <span className="stock-price">{formatCurrency(stock.price, stock.currency)}</span>
      </div>
      <div className={`stock-change ${isPositive ? 'positive' : 'negative'}`}>
        {isPositive ? '▲' : '▼'} {stock.change} ({stock.change_percent}%)
      </div>
    </div>
  );
};

export default TopStockCard;