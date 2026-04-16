import { useEffect, useState } from 'react'
import axios from 'axios'
import KpiCard from '../components/KpiCard'

const API = 'http://localhost:8000'

export default function Dashboard() {
  const [risco, setRisco]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get(`${API}/kpis/risco`)
      .then(r => setRisco(r.data.dados))
      .catch(() => setRisco(null))
      .finally(() => setLoading(false))
  }, [])

  const total  = risco ? risco.reduce((s, r) => s + r[1], 0) : 0
  const get    = (label) => risco?.find(r => r[0] === label)?.[1] ?? 0
  const highPct = total ? ((get('High_Risk') / total) * 100).toFixed(1) : 0

  return (
    <div>
      <div className="page-header">
        <div className="page-title">// DASHBOARD</div>
        <div className="page-sub">Visão geral das operações de supply chain</div>
      </div>

      {loading ? (
        <div className="loading">Carregando dados...</div>
      ) : (
        <>
          <div className="cards-grid">
            <KpiCard label="Total de Registros" value={total.toLocaleString('pt-BR')} sub="registros no banco" />
            <KpiCard label="High Risk"     value={get('High_Risk').toLocaleString('pt-BR')}     sub={`${highPct}% do total`} variant="danger" />
            <KpiCard label="Moderate Risk" value={get('Moderate_Risk').toLocaleString('pt-BR')} sub="risco moderado"         variant="warn" />
            <KpiCard label="Low Risk"      value={get('Low_Risk').toLocaleString('pt-BR')}      sub="operações estáveis"     variant="ok" />
          </div>

          <div className="table-wrap">
            <div className="table-head">Distribuição por Classificação de Risco</div>
            <table>
              <thead>
                <tr>
                  <th>Classificação</th>
                  <th>Total</th>
                  <th>Percentual</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {risco && risco.map(([label, count]) => (
                  <tr key={label}>
                    <td>{label}</td>
                    <td>{count.toLocaleString('pt-BR')}</td>
                    <td>{total ? ((count / total) * 100).toFixed(1) : 0}%</td>
                    <td>
                      <span className={`badge ${
                        label === 'High_Risk'     ? 'badge-danger' :
                        label === 'Moderate_Risk' ? 'badge-warn'   : 'badge-ok'
                      }`}>{label}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}