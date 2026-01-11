// src/components/TickerTape.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import './TickerTape.css';

const TickerTape = () => {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    const fetchTopStocks = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/market/top-stocks');
        // We duplicate the data to create a seamless loop
        setStocks([...response.data, ...response.data]);
      } catch (error) {
        console.error("Failed to fetch stocks for ticker tape", error);
      }
    };
    fetchTopStocks();
  }, []);

  if (stocks.length === 0) return null;

  return (
    <div className="ticker-wrap">
      <div className="ticker-move">
        {stocks.map((stock, index) => {
          const isPositive = stock.change >= 0;
          return (
            <div className="ticker-item" key={index}>
              <span className="ticker-symbol">{stock.ticker}</span>
              <span className="ticker-price">${stock.price.toFixed(2)}</span>
              <span className={`ticker-change ${isPositive ? 'positive' : 'negative'}`}>
                {isPositive ? '▲' : '▼'} {stock.change.toFixed(2)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TickerTape;