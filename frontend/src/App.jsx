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

      setData(result);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const scout = data?.architect_scout;

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

      {error && <div className="error-banner">{error}</div>}

      {data && (
        <div className="dashboard">
          <section className="grid grid-4">
            <SummaryCard title="Repository Path" value={data.repo_path} />
            <SummaryCard title="File Count" value={String(data.file_count)} />
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
              files={data.selected_files || []}
            />
            <FileListCard
              title="Scout Important Files"
              files={(scout?.important_files || []).map((item) =>
                typeof item === "string" ? item : `${item.path} — ${item.reason}`
              )}
            />
          </section>

          <section className="grid grid-2">
            <MarkdownCard
              title="Architecture Summary"
              content={data.architect_summary || "No summary available."}
            />
            <MarkdownCard
              title="Reviewer Summary"
              content={data.reviewer_summary || "No review available."}
            />
          </section>

          <section>
            <MarkdownCard
              title="Repository Tree"
              content={
                "```text\n" + (data.tree || "No tree available.") + "\n```"
              }
            />
          </section>
        </div>
      )}
    </div>
  );
}