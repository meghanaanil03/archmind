import { useState } from "react";
import AnalyzeForm from "./components/AnalyzeForm";
import SummaryCard from "./components/SummaryCard";
import FileListCard from "./components/FileListCard";
import MarkdownCard from "./components/MarkdownCard";
import "./index.css";

const API_URL = "http://127.0.0.1:8000/analyze/local";

export default function App() {
  const [repoPath, setRepoPath] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setData(null);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ repo_path: repoPath }),
      });

      const result = await res.json();

      if (!res.ok) {
        throw new Error(result.detail || "Analysis failed");
      }

      console.log("API result:", result);
      setData(result);
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const scout = data?.architect_scout || {};
  const selectedFiles = Array.isArray(data?.selected_files) ? data.selected_files : [];
  const importantFiles = Array.isArray(scout?.important_files) ? scout.important_files : [];

  const architectSummary =
    typeof data?.architect_summary === "string"
      ? data.architect_summary
      : JSON.stringify(data?.architect_summary, null, 2);

  const reviewerSummary =
    typeof data?.reviewer_summary === "string"
      ? data.reviewer_summary
      : JSON.stringify(data?.reviewer_summary, null, 2);

  const repoTree =
    typeof data?.tree === "string" ? data.tree : "No tree available.";

  const importantFileDisplay = importantFiles.map((item, index) => {
    if (typeof item === "string") return item;
    if (item && typeof item === "object") {
      return `${item.path || `File ${index + 1}`} — ${item.reason || "No reason provided"}`;
    }
    return String(item);
  });

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>ArchMind</h1>
        <p>Multi-agent codebase intelligence platform</p>
      </header>

      <AnalyzeForm
        repoPath={repoPath}
        setRepoPath={setRepoPath}
        onSubmit={handleAnalyze}
        loading={loading}
      />

      {loading && <div className="card">Analyzing repository...</div>}
      {error && <div className="error-banner">{error}</div>}

      {data && (
        <div className="dashboard">
          <section className="grid grid-4">
            <SummaryCard title="Repository Path" value={data.repo_path || "N/A"} />
            <SummaryCard title="File Count" value={String(data.file_count ?? "N/A")} />
            <SummaryCard
              title="Project Type"
              value={scout?.project_type || "Unknown"}
            />
            <SummaryCard
              title="Architecture Guess"
              value={scout?.architecture_guess || "Unknown"}
            />
          </section>

          <section className="grid grid-2">
            <FileListCard
              title="Selected Files"
              files={selectedFiles}
            />
            <FileListCard
              title="Scout Important Files"
              files={importantFileDisplay}
            />
          </section>

          <section className="grid grid-2">
            <MarkdownCard
              title="Architecture Summary"
              content={architectSummary || "No summary available."}
            />
            <MarkdownCard
              title="Reviewer Summary"
              content={reviewerSummary || "No review available."}
            />
          </section>

          <section>
            <MarkdownCard
              title="Repository Tree"
              content={"```text\n" + repoTree + "\n```"}
            />
          </section>
        </div>
      )}
    </div>
  );
}