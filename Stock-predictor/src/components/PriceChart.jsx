// src/components/PriceChart.jsx
import { useState, useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

const chartBgPlugin = {
  id: 'customCanvasBackgroundColor',
  beforeDraw: (chart, args, options) => {
    const {ctx} = chart;
    ctx.save();
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = options.color || '#0d1117';
    ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  }
};

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler, chartBgPlugin
);

const PriceChart = ({ chartData, ticker }) => {
  const [data, setData] = useState({ datasets: [] });
  const chartRef = useRef(null);

  useEffect(() => {
    const chart = chartRef.current;

    if (!chart || !chartData || !chartData.datasets) {
      return;
    }

    // Check if this is a Monte Carlo chart (if it has 'fill' properties, it's MC)
    const isMonteCarlo = chartData.datasets.some(d => d.fill !== undefined);

    const createGradient = (ctx) => {
      const gradient = ctx.createLinearGradient(0, chart.height, 0, 0);
      gradient.addColorStop(0, 'rgba(88, 166, 255, 0)');
      gradient.addColorStop(1, 'rgba(88, 166, 255, 0.5)');
      return gradient;
    };
    
    // Apply gradient only if it's NOT a Monte Carlo chart (which uses solid fills for intervals)
    if (!isMonteCarlo) {
      setData({
        ...chartData,
        datasets: chartData.datasets.map(dataset => ({
          ...dataset,
          backgroundColor: createGradient(chart.ctx),
        })),
      });
    } else {
        setData(chartData); // Use the data as is for Monte Carlo (with fills)
    }
  }, [chartData]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      customCanvasBackgroundColor: { color: 'rgba(13, 17, 23, 0.8)' },
      legend: { 
        position: 'top', 
        labels: { 
          color: '#e6edf3', 
          font: { size: 14, family: "'Poppins', sans-serif" },
          // --- Custom filter for Monte Carlo legends ---
          filter: function(legendItem, chartData) {
            // Hide specific 'Lower' labels or simulation labels
            if (legendItem.text.includes('(Lower)') || legendItem.text.includes('Sim ')) {
              return false;
            }
            return true;
          }
        } 
      },
      title: { display: true, text: ticker, color: '#ffffff', font: { size: 18, family: "'Poppins', sans-serif" } },
      tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
              label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                      label += ': ';
                  }
                  if (context.parsed.y !== null) {
                      label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                  }
                  return label;
              }
          }
      }
    },
    scales: {
      x: { ticks: { color: '#c9d1d9' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
      y: { ticks: { color: '#c9d1d9' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
    }
  };

  return (
    <div style={{ position: 'relative', height: '400px', width: '100%' }}>
      <Line ref={chartRef} options={options} data={data} />
    </div>
  );
};

export default PriceChart;