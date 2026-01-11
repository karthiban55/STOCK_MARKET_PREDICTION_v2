// src/pages/PredictPage.jsx
import { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import PredictionCard from '../components/PredictionCard';
import NewsList from '../components/NewsList';
import PriceChart from '../components/PriceChart';
import DateRangeSelector from '../components/DateRangeSelector';
import LivePriceCard from '../components/LivePriceCard';
import LoadingIndicator from '../components/LoadingIndicator';

const PredictPage = () => {
  const [searchInput, setSearchInput] = useState('RELIANCE.NS');
  const [searchResults, setSearchResults] = useState([]);
  const [analysisData, setAnalysisData] = useState(null);
  const [liveData, setLiveData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [period, setPeriod] = useState('1y');

  const predictionSteps = [
    "Fetching live market data...",
    "Analyzing news sentiment...",
    "Calculating technical indicators...",
    "Training prediction model...",
    "Forecasting next-day price...",
  ];

  const handleSearch = async () => {
    if (!searchInput) {
      setError('Please enter a company name or ticker.');
      return;
    }
    setLoading(true);
    setError('');
    setAnalysisData(null);
    setLiveData(null);
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
    setAnalysisData(null);
    setLiveData(null);
    setSearchResults([]);
    try {
      const tickerToUpper = ticker.toUpperCase();
      const analysisRequest = axios.get(`http://127.0.0.1:8000/analyze/${tickerToUpper}`, { params: { period } });
      const liveRequest = axios.get(`http://127.0.0.1:8000/live/${tickerToUpper}`);
      const [analysisResponse, liveResponse] = await Promise.all([analysisRequest, liveRequest]);
      setAnalysisData(analysisResponse.data);
      setLiveData(liveResponse.data);
    } catch (err) {
      setError(`Failed to fetch all data for ${ticker.toUpperCase()}.`);
    } finally {
      setLoading(false);
    }
  };

  const handlePeriodChange = (newPeriod) => {
    setPeriod(newPeriod);
    if (analysisData) {
      handleSelectTicker(analysisData.ticker);
    }
  };
  
  const containerVariants = { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: 0.1 } } };
  const itemVariants = { hidden: { y: 20, opacity: 0 }, visible: { y: 0, opacity: 1 } };

  return (
    <div className="page-container">
      <motion.div initial={{ y: -20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.5 }}>
        <h2>Prediction & Analysis Dashboard</h2>
        <p className="page-description">Enter a company name or ticker to get a next-day price prediction and sentiment analysis.</p>
        <SearchBar ticker={searchInput} setTicker={setSearchInput} onSearch={handleSearch} />
      </motion.div>
      
      {loading && <LoadingIndicator steps={predictionSteps} />}
      {error && <p className="error">{error}</p>}
      
      <AnimatePresence>
        {searchResults.length > 0 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <SearchResults results={searchResults} onSelectTicker={handleSelectTicker} />
          </motion.div>
        )}
      </AnimatePresence>
      
      <AnimatePresence>
        {analysisData && liveData && (
          <motion.div className="results-grid" variants={containerVariants} initial="hidden" animate="visible">
            <motion.div className="main-content" variants={itemVariants}>
              <LivePriceCard liveData={liveData} />
              <PriceChart chartData={liveData.intraday_chart} ticker={`${liveData.ticker} (Intraday)`} />
              <hr style={{borderColor: "rgba(255, 255, 255, 0.1)", margin: "2rem 0"}} />
              <DateRangeSelector selectedPeriod={period} onSelectPeriod={handlePeriodChange} />
              <PriceChart chartData={analysisData.chart_data.price_chart} ticker={`${analysisData.ticker} (Historical)`} />
            </motion.div>
            <motion.div className="sidebar" variants={containerVariants}>
              <motion.div variants={itemVariants}>
                <PredictionCard prediction={analysisData.prediction} sentiment={analysisData.sentiment} ticker={analysisData.ticker} />
              </motion.div>
              <motion.div variants={itemVariants}>
                <NewsList headlines={analysisData.sentiment.headlines} />
              </motion.div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PredictPage;