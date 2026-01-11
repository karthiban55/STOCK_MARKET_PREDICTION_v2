// src/components/NewsList.jsx
const NewsList = ({ headlines }) => {
  return (
    <div className="card news-list">
      <h3>Recent News</h3>
      <ul>
        {headlines.slice(0, 5).map((article, index) => (
          <li key={index}>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              {article.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NewsList;