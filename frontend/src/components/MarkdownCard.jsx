import ReactMarkdown from "react-markdown";

export default function MarkdownCard({ title, content }) {
  return (
    <div className="card markdown-card">
      <h3>{title}</h3>
      <div className="markdown-body">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
}