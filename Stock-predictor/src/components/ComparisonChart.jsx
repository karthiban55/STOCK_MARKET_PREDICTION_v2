// src/components/ComparisonChart.jsx
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
  CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, chartBgPlugin
);

const ComparisonChart = ({ chartData }) => {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      customCanvasBackgroundColor: { color: 'rgba(13, 17, 23, 0.8)' },
      legend: { position: 'top', labels: { color: '#e6edf3', font: { size: 14, family: "'Poppins', sans-serif" } } },
      title: { display: true, text: 'Normalized Stock Performance Comparison (%)', color: '#ffffff', font: { size: 18, family: "'Poppins', sans-serif" } },
    },
    scales: {
      x: { ticks: { color: '#c9d1d9' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
      y: { ticks: { color: '#c9d1d9', callback: function(value) { return value + '%'; } }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
    }
  };

  // --- FIX: Wrap the chart in a div with a defined height ---
  return (
    <div style={{ position: 'relative', height: '500px', width: '100%' }}>
      <Line options={options} data={chartData} />
    </div>
  );
};

export default ComparisonChart;