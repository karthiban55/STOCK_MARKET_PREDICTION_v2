// src/pages/HomePage.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

import TopStockCard from '../components/TopStockCard';
import './HomePage.css';

const HomePage = () => {
  const [topStocks, setTopStocks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopStocks = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/market/top-stocks');
        setTopStocks(response.data);
      } catch (error) {
        console.error("Failed to fetch top stocks", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTopStocks();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2, delayChildren: 0.3 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <motion.div 
      className="home-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <section className="hero-section">
        <motion.div 
          className="hero-content"
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <p className="subtitle">THE FUTURE OF ANALYSIS</p>
          <h1 className="title">Data Beats Intuition. Insight Beats Data.</h1>
          <p className="description">
            Welcome to MarketPulse. Our AI-driven platform goes beyond the numbers, providing predictive insights, sentiment analysis, and risk assessment to help you navigate the market with confidence.
          </p>
          <Link to="/predict" className="cta-button">Start Analyzing</Link>
        </motion.div>
        <motion.div 
          className="hero-graphic"
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1, delay: 0.5, type: "spring" }}
        >
          <div className="sphere">
            <div className="sphere-inner"></div>
          </div>
        </motion.div>
      </section>

      <section className="market-movers-section">
        <h3>Today's Market Movers</h3>
        {loading ? (
          <p className="loading">Loading top stocks...</p>
        ) : (
          <motion.div 
            className="top-stocks-grid"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {topStocks.map(stock => (
              <motion.div key={stock.ticker} variants={itemVariants}>
                <TopStockCard stock={stock} />
              </motion.div>
            ))}
          </motion.div>
        )}
      </section>
    </motion.div>
  );
};

export default HomePage;