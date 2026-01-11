// src/pages/RiskPage.jsx
import { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import PriceChart from '../components/PriceChart';
import LoadingIndicator from '../components/LoadingIndicator';
import './RiskPage.css';

const MetricCard = ({ label, value }) => (
  <motion.div className="metric-card" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.5 }}>
    <span className="label">{label}</span>
    <span className="value">{value}</span>
  </motion.div>
);

const RiskPage = () => {
  const [searchInput, setSearchInput] = useState('RELIANCE.NS');
  const [searchResults, setSearchResults] = useState([]);
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const riskSteps = [
    "Fetching 5 years of market data...",
    "Calculating volatility and beta...",
    "Computing Sharpe & Sortino ratios...",
    "Running 1000 future-path simulations...",
    "Visualizing Monte Carlo results..."
  ];

  const handleSearch = async () => {
    if (!searchInput) {
      setError('Please enter a company name or ticker.');
      return;
    }
    setLoading(true);
    setError('');
    setRiskData(null);
    setSearchResults([]);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/search/${searchInput}`);
      const results = response.data.results;
      if (results.length > 0) {
        setSearchResults(results);
      } else {
        handleSelectTicker(searchInput);
      }
    } catch (err) {
      setError('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTicker = async (ticker) => {
    setLoading(true);
    setError('');
    setRiskData(null);
    setSearchResults([]);
    try {
      const tickerToUpper = ticker.toUpperCase();
      const response = await axios.get(`http://127.0.0.1:8000/risk/${tickerToUpper}`);
      setRiskData(response.data);
    } catch (err) {
      setError(`Failed to fetch risk assessment for ${ticker.toUpperCase()}.`);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="page-container risk-page">
      <h2>Advanced Risk Assessment</h2>
      <p className="page-description">Analyze a stock's volatility, risk-adjusted returns, and potential future paths with a Monte Carlo simulation.</p>
      
      <SearchBar ticker={searchInput} setTicker={setSearchInput} onSearch={handleSearch} />
      {searchResults.length > 0 && <SearchResults results={searchResults} onSelectTicker={handleSelectTicker} />}

      {loading && <LoadingIndicator steps={riskSteps} />}
      {error && <p className="error">{error}</p>}

      {riskData && (
        <div>
          <div className="metrics-grid">
            <MetricCard label="Annualized Volatility" value={`${riskData.risk_metrics.annualized_volatility}%`} />
            <MetricCard label="Beta (vs. S&P 500)" value={riskData.risk_metrics.beta} />
            <MetricCard label="Sharpe Ratio" value={riskData.risk_metrics.sharpe_ratio} />
            <MetricCard label="Sortino Ratio" value={riskData.risk_metrics.sortino_ratio} />
          </div>

          <motion.div className="simulation-container" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5, duration: 0.8 }}>
            <PriceChart chartData={riskData.monte_carlo_chart} ticker={`90-Day Monte Carlo Simulation for ${riskData.ticker}`} />
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default RiskPage;