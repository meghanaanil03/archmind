import { useState } from "react";
import AnalyzeForm from "./components/AnalyzeForm";
import SummaryCard from "./components/SummaryCard";
import FileListCard from "./components/FileListCard";
import MarkdownCard from "./components/MarkdownCard";
import Tabs from "./components/Tabs";

import "./styles/base.css";
import "./styles/layout.css";
import "./styles/components.css";
import "./styles/markdown.css";

const API_URL = "http://127.0.0.1:8000/analyze/local";

export default function App() {
  const [repoPath, setRepoPath] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

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
      setActiveTab("overview");
    } catch (err) {
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
      : JSON.stringify(data?.architect_summary ?? {}, null, 2);

  const reviewerSummary =
    typeof data?.reviewer_summary === "string"
      ? data.reviewer_summary
      : JSON.stringify(data?.reviewer_summary ?? {}, null, 2);

  const repoTree =
    typeof data?.tree === "string" ? data.tree : "No tree available.";

  const importantFileDisplay = importantFiles.map((item, index) => {
    if (typeof item === "string") return item;
    if (item && typeof item === "object") {
      return `${item.path || `File ${index + 1}`} — ${item.reason || "No reason provided"}`;
    }
    return String(item);
  });

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "architecture", label: "Architecture" },
    { id: "review", label: "Review" },
    { id: "tree", label: "Repository Tree" },
  ];

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

      {loading && <div className="status-card">Analyzing repository...</div>}
      {error && <div className="error-banner">{error}</div>}

      {data && (
        <div className="dashboard">
          <section className="grid grid-4">
            <SummaryCard title="Repository Path" value={data.repo_path || "N/A"} />
            <SummaryCard title="File Count" value={String(data.file_count ?? "N/A")} />
            <SummaryCard title="Project Type" value={scout?.project_type || "Unknown"} />
            <SummaryCard title="Architecture Guess" value={scout?.architecture_guess || "Unknown"} />
          </section>

          <Tabs tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

          {activeTab === "overview" && (
            <section className="grid grid-2">
              <FileListCard title="Selected Files" files={selectedFiles} />
              <FileListCard title="Scout Important Files" files={importantFileDisplay} />
            </section>
          )}

          {activeTab === "architecture" && (
            <section className="single-panel">
              <MarkdownCard
                title="Architecture Summary"
                content={architectSummary || "No summary available."}
              />
            </section>
          )}

          {activeTab === "review" && (
            <section className="single-panel">
              <MarkdownCard
                title="Reviewer Summary"
                content={reviewerSummary || "No review available."}
              />
            </section>
          )}

          {activeTab === "tree" && (
            <section className="single-panel">
              <div className="card tree-card">
                <h3>Repository Tree</h3>
                <pre className="tree-block">{repoTree}</pre>
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}