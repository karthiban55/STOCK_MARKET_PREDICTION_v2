// src/components/SearchResults.jsx
import './SearchResults.css';

const SearchResults = ({ results, onSelectTicker }) => {
  if (results.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <ul className="search-results">
      {results.map((item) => (
        <li key={item.ticker}>
          <button onClick={() => onSelectTicker(item.ticker)}>
            <span className="ticker">{item.ticker}</span>
            <span className="name">{item.name}</span>
          </button>
        </li>
      ))}
    </ul>
  );
};

export default SearchResults;