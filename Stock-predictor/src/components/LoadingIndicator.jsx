// src/components/LoadingIndicator.jsx
import { useState, useEffect } from 'react';
import './LoadingIndicator.css';

// A default message if no specific steps are provided
const defaultSteps = [
  "Initializing analysis...",
  "Contacting data sources...",
  "Compiling results..."
];

const LoadingIndicator = ({ steps = defaultSteps }) => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // This interval will cycle through the analysis steps
    const interval = setInterval(() => {
      setCurrentStep((prevStep) => (prevStep + 1) % steps.length);
    }, 1500); // Change text every 1.5 seconds

    // Cleanup the interval when the component is removed
    return () => clearInterval(interval);
  }, [steps]); // Effect re-runs if the steps change

  return (
    <div className="loading-container">
      <div className="pulse-animation">
        <div className="pulse-dot"></div>
        <div className="pulse-dot"></div>
        <div className="pulse-dot"></div>
      </div>
      <p className="loading-text">{steps[currentStep]}</p>
    </div>
  );
};

export default LoadingIndicator;