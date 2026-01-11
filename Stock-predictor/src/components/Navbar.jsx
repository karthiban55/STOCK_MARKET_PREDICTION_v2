// src/components/Navbar.jsx
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <NavLink to="/" className="nav-logo">
        MarketPulse
      </NavLink>
      <ul className="nav-menu">
        <li><NavLink to="/predict">Predict</NavLink></li>
        <li><NavLink to="/compare">Compare</NavLink></li>
        <li><NavLink to="/news">News</NavLink></li>
        <li><NavLink to="/risk">Risk</NavLink></li>
        
        {/* --- NEW LINK ADDED HERE --- */}
        <li><NavLink to="/strategy">Strategy</NavLink></li>

      </ul>
    </nav>
  );
};

export default Navbar;