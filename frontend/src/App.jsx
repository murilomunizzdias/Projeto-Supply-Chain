import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Alertas from './pages/Alertas'
import Simulador from './pages/Simulador'
import './App.css'

const NAV = [
  { id: 'Dashboard', label: 'Dashboard', icon: '▦' },
  { id: 'Alertas',   label: 'Alertas',   icon: '⚠' },
  { id: 'Simulador', label: 'Simulador', icon: '⟳' },
]

export default function App() {
  const [page, setPage] = useState('dashboard')

  return (
    <div className="app">
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
        </nav>
        <div className="sidebar-footer">
          <div className="status-dot"></div>
          <span>API conectada</span>
        </div>
      </aside>

      <main className="content">
        {page === 'Dashboard'  && <Dashboard />}
        {page === 'Alertas'    && <Alertas />}
        {page === 'Simulador'  && <Simulador />}
      </main>
    </div>
  )
}