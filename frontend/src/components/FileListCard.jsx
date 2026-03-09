export default function FileListCard({ title, files }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {files.length === 0 ? (
        <p className="muted">No files available.</p>
      ) : (
        <ul className="file-list">
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ul>
      )}
    </div>
  );
}