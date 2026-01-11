import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import TickerTape from './components/TickerTape';
import HomePage from './pages/HomePage';
import PredictPage from './pages/PredictPage';
import ComparePage from './pages/ComparePage';
import RiskPage from './pages/RiskPage';
import NewsPage from './pages/NewsPage';

// --- NEW: Import the StrategyPage ---
import StrategyPage from './pages/StrategyPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <TickerTape />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/predict" element={<PredictPage />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/risk" element={<RiskPage />} />
          <Route path="/news" element={<NewsPage />} />
          
          {/* --- NEW: Add the Strategy route --- */}
          <Route path="/strategy" element={<StrategyPage />} />
          
        </Routes>
      </main>
    </div>
  );
}

export default App;