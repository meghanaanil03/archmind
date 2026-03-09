export default function AnalyzeForm({
  repoPath,
  setRepoPath,
  onSubmit,
  loading,
}) {
  return (
    <form className="analyze-form" onSubmit={onSubmit}>
      <input
        type="text"
        placeholder="Enter local repository path..."
        value={repoPath}
        onChange={(e) => setRepoPath(e.target.value)}
      />
      <button type="submit" disabled={loading || !repoPath.trim()}>
        {loading ? "Analyzing..." : "Analyze Repository"}
      </button>
    </form>
  );
}