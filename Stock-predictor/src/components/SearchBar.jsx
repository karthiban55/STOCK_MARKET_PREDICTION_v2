// src/components/SearchBar.jsx
const SearchBar = ({ ticker, setTicker, onSearch }) => {
  return (
    <div className="search-bar">
      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value.toUpperCase())}
        placeholder="Enter Stock Ticker (e.g., AAPL)"
      />
      <button onClick={onSearch}>Analyze</button>
    </div>
  );
};

export default SearchBar;