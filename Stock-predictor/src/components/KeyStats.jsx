// src/components/KeyStats.jsx
import './KeyStats.css';

const formatNumber = (num) => {
  if (num === null || num === undefined) return 'N/A';
  if (num > 1_000_000_000_000) return `${(num / 1_000_000_000_000).toFixed(2)}T`;
  if (num > 1_000_000_000) return `${(num / 1_000_000_000).toFixed(2)}B`;
  if (num > 1_000_000) return `${(num / 1_000_000).toFixed(2)}M`;
  return num.toLocaleString();
};

const StatItem = ({ label, value }) => (
  <div className="stat-item">
    <span className="stat-label">{label}</span>
    <span className="stat-value">{value}</span>
  </div>
);

const KeyStats = ({ stats }) => {
  return (
    <div className="key-stats-container">
      <h3 className="stats-title">Key Statistics</h3>
      <div className="key-stats-grid">
        <StatItem label="Open" value={stats.open?.toFixed(2) || 'N/A'} />
        <StatItem label="Market Cap" value={formatNumber(stats.marketCap)} />
        <StatItem label="High" value={stats.dayHigh?.toFixed(2) || 'N/A'} />
        <StatItem label="P/E Ratio" value={stats.trailingPE?.toFixed(2) || 'N/A'} />
        <StatItem label="Low" value={stats.dayLow?.toFixed(2) || 'N/A'} />
        <StatItem label="Div Yield" value={stats.dividendYield ? `${(stats.dividendYield * 100).toFixed(2)}%` : 'N/A'} />
        <StatItem label="52-wk high" value={stats.fiftyTwoWeekHigh?.toFixed(2) || 'N/A'} />
        <StatItem label="Volume" value={formatNumber(stats.volume)} />
        <StatItem label="52-wk low" value={stats.fiftyTwoWeekLow?.toFixed(2) || 'N/A'} />
        <StatItem label="Avg. Volume" value={formatNumber(stats.averageVolume)} />
      </div>
    </div>
  );
};

export default KeyStats;