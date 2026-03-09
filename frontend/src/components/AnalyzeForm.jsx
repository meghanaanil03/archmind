export default function AnalyzeForm({
  repoPath,
  setRepoPath,
  onSubmit,
  loading,
}) {
  const safeRepoPath = repoPath || "";

  return (
    <form className="analyze-form" onSubmit={onSubmit}>
      <input
        type="text"
        placeholder="Enter local repository path..."
        value={safeRepoPath}
        onChange={(e) => setRepoPath(e.target.value)}
      />
      <button type="submit" disabled={loading || !safeRepoPath.trim()}>
        {loading ? "Analyzing..." : "Analyze Repository"}
      </button>
    </form>
  );
}