// src/components/DateRangeSelector.jsx
import './DateRangeSelector.css';

const DateRangeSelector = ({ selectedPeriod, onSelectPeriod }) => {
  const periods = ['30d', '6mo', '1y', '5y', 'max'];

  return (
    <div className="range-selector">
      {periods.map((period) => (
        <button
          key={period}
          className={selectedPeriod === period ? 'active' : ''}
          onClick={() => onSelectPeriod(period)}
        >
          {period.toUpperCase()}
        </button>
      ))}
    </div>
  );
};

export default DateRangeSelector;