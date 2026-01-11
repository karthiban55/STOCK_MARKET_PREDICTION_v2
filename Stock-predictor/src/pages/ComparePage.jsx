// src/pages/ComparePage.jsx
import { useState } from 'react';
import axios from 'axios';
import ComparisonChart from '../components/ComparisonChart';

const ComparePage = () => {
  const [tickersInput, setTickersInput] = useState('AAPL,MSFT,TSLA');
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

// src/pages/ComparePage.jsx

const handleCompare = async () => {
    setLoading(true);
    setError('');
    setChartData(null);

    const tickers = tickersInput.split(',').map(t => t.trim()).filter(Boolean);

    // --- ADD THIS VALIDATION BLOCK ---
    if (tickers.length < 2 || tickers.length > 4) {
      setError('Please enter between 2 and 4 tickers to compare.');
      setLoading(false);
      return; // Stop the function here
    }
    // --- END OF NEW BLOCK ---

    try {
      const response = await axios.get('http://127.0.0.1:8000/compare/', {
        params: { tickers },
      });
      setChartData(response.data);
    } catch (err) {
      setError('Failed to fetch comparison data. Please check the tickers.');
      console.error(err);
    } finally {
      setLoading(false);
    }
};
  return (
    <div className="page-container">
      <h2>Stock Performance Comparison</h2>
      <p className="page-description">
        Enter 2-4 stock tickers separated by commas to compare their normalized performance over the last year.
      </p>
      
      {/* Reusing styles from the original SearchBar */}
      <div className="search-bar">
        <input
          type="text"
          value={tickersInput}
          onChange={(e) => setTickersInput(e.target.value.toUpperCase())}
          placeholder="e.g., AAPL, MSFT, GOOGL"
        />
        <button onClick={handleCompare} disabled={loading}>
          {loading ? 'Comparing...' : 'Compare'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      
      {chartData && (
        <div className="main-content">
          <ComparisonChart chartData={chartData} />
        </div>
      )}
    </div>
  );
};

export default ComparePage;