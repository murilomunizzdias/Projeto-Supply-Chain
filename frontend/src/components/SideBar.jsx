const NAV = [
  { id: 'dashboard', label: 'Dashboard', icon: '▦' },
  { id: 'alertas',   label: 'Alertas',   icon: '⚠' },
  { id: 'simulador', label: 'Simulador', icon: '⟳' },
]

export default function Sidebar({ page, setPage }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <span className="brand-icon">⬡</span>
        <div>
          <div className="brand-title">SupplyChain</div>
          <div className="brand-sub">Monitor de Operações</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {NAV.map(n => (
          <button
            key={n.id}
            className={`nav-item ${page === n.id ? 'active' : ''}`}
            onClick={() => setPage(n.id)}
          >
            <span className="nav-icon">{n.icon}</span>
            <span>{n.label}</span>
          </button>
        ))}
        <a
          href="http://localhost:8501"
          target="_blank"
          rel="noreferrer"
          className="nav-item"
          style={{ textDecoration: 'none',
                    display:'_blank',
                    allignItems:'center',
                    color: 'var(--muted)'
           }}
        >
          <span className="nav-icon">📊</span>
          <span>Dashboard Avançado</span>
        </a>
      </nav>
      <div className="sidebar-footer">
        <div className="status-dot"></div>
        <span>API conectada</span>
      </div>
    </aside>
  )
}