export default function Tabs({ tabs, activeTab, onTabChange }) {
  return (
    <div className="tabs-shell">
      <div className="tabs-list">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={`tab-button ${activeTab === tab.id ? "active" : ""}`}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
}