// src/pages/StrategyPage.jsx
import React, { useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Scatter, ComposedChart
} from 'recharts';
import './StrategyPage.css'; // Use the CSS file you created

// A component to render the "BUY" or "SELL" dot on the chart
const SignalDot = (props) => {
  const { cx, cy, payload } = props;
  if (payload.type === 'BUY') {
    return <circle cx={cx} cy={cy} r={5} fill="#4CAF50" stroke="#fff" strokeWidth={2} />;
  }
  if (payload.type === 'SELL') {
    return <circle cx={cx} cy={cy} r={5} fill="#F44336" stroke="#fff" strokeWidth={2} />;
  }
  return null;
};

const StrategyPage = () => {
  const [ticker, setTicker] = useState('RELIANCE.NS');
  const [strategy, setStrategy] = useState('rsi'); // 'rsi' or 'macd'
  const [backtestData, setBacktestData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRunBacktest = async () => {
    console.log('--- handleRunBacktest started ---');
    setLoading(true);
    setError('');
    setBacktestData(null);
    setChartData([]);

    try {
      const response = await axios.get(`http://127.0.0.1:8000/strategy/backtest/${ticker.toUpperCase()}`, {
        params: { strategy }
      });

      // --- DEBUGGING LOGS ---
      console.log('API Response Received:', response.data);
      const { backtest_results, price_data } = response.data;
      
      console.log('Backtest Results (Metrics):', backtest_results);
      console.log('Price Data (for chart):', price_data);

      // Set the metrics first
      setBacktestData(backtest_results);

      // --- Format data for the chart ---
      const signalsMap = new Map(
        backtest_results.signals.map(s => [s.date, s])
      );
      console.log('Signals Map created:', signalsMap);

      const combinedData = price_data.map(pricePoint => {
        const date = pricePoint.Date; 
        const signal = signalsMap.get(date);
        
        return {
          date: date,
          Close: pricePoint.Close,
          type: signal ? signal.type : null,
          signalPrice: signal ? signal.price : null
        };
      });

      console.log('Combined Chart Data:', combinedData);
      setChartData(combinedData);
      // --- END DEBUGGING ---

    } catch (err) {
      console.error('Error during backtest:', err); // Log the full error
      const errorMsg = err.response?.data?.detail || 'Failed to run backtest.';
      setError(errorMsg);
    } finally {
      console.log('--- handleRunBacktest finished ---');
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h2>Strategy Backtesting Lab</h2>
      <p className="page-description">Test trading strategies against historical data.</p>
      
      <div className="search-bar" style={{ marginBottom: '2rem' }}>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="E.g., RELIANCE.NS"
        />
        <select value={strategy} onChange={(e) => setStrategy(e.target.value)} style={{ marginLeft: '1rem', padding: '0.5rem' }}>
          <option value="rsi">RSI Strategy (30/70)</option>
          <option value="macd">MACD Crossover Strategy</option>
        </select>
        <button onClick={handleRunBacktest} disabled={loading} style={{ marginLeft: '1rem' }}>
          {loading ? 'Running...' : 'Run Backtest'}
        </button>
      </div>

      {loading && <p>Running backtest...</p>}
      {error && <p className="error">{error}</p>}
      
      {/* This checks if backtestData (the metrics) is loaded */}
      {backtestData && (
        <div className="strategy-results">
          <h3>Backtest Results ({backtestData.metrics.strategy_name})</h3>
          <div className="results-metrics">
            <p>Initial Capital: <strong>${backtestData.metrics.initial_capital.toLocaleString()}</strong></p>
            <p>Final Value: <strong>${backtestData.metrics.final_value.toLocaleString()}</strong></p>
            <p>Total Return: 
              <strong style={{ color: backtestData.metrics.total_return_pct >= 0 ? '#4CAF50' : '#F44336' }}>
                {backtestData.metrics.total_return_pct}%
              </strong>
            </p>
          </div>
          
          {/* This checks if the chartData (the line) is loaded */}
          {chartData.length > 0 && (
            <div className="chart-container" style={{ width: '100%', height: 400, marginTop: '2rem' }}>
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart
                  data={chartData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.1} />
                  <XAxis dataKey="date" angle={-20} textAnchor="end" height={50} interval={Math.floor(chartData.length / 10)} />
                  <YAxis domain={['auto', 'auto']} allowDataOverflow={true} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="Close" 
                    stroke="#8884d8" 
                    strokeWidth={2} 
                    dot={false}
                  />
                  <Scatter 
                    name="Buy/Sell Signals" 
                    dataKey="signalPrice" 
                    shape={<SignalDot />} 
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default StrategyPage;