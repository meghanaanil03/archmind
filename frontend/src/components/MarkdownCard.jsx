import ReactMarkdown from "react-markdown";

export default function MarkdownCard({ title, content }) {
  const safeContent =
    typeof content === "string" ? content : JSON.stringify(content, null, 2);

  return (
    <div className="card markdown-card">
      <h3>{title}</h3>
      <div className="markdown-body">
        <ReactMarkdown>{safeContent}</ReactMarkdown>
      </div>
    </div>
  );
}