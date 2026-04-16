import { useEffect, useState } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000'

export default function AlertaCard({ config }) {
  const [dados, setDados]     = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get(`${API}${config.endpoint}`)
      .then(r => {
        const val = Object.values(r.data)[0]
        setDados(Array.isArray(val) ? val : [])
      })
      .catch(() => setDados([]))
      .finally(() => setLoading(false))
  }, [])

  const count = dados?.length ?? 0

  return (
    <div className="table-wrap">
      <div className="table-head" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>{config.label}</span>
        <span className={`badge ${count > 0 ? 'badge-danger' : 'badge-ok'}`}>
          {count > 0 ? `${count} alertas` : 'Normal'}
        </span>
      </div>
      {loading ? (
        <div className="loading" style={{ padding: '16px 20px' }}>Carregando...</div>
      ) : count === 0 ? (
        <div style={{ padding: '14px 20px', fontSize: '12px', color: 'var(--muted)', fontFamily: 'var(--font-mono)' }}>
          Nenhum alerta ativo para este indicador.
        </div>
      ) : (
        <table>
          <thead>
            <tr>{config.cols.map(c => <th key={c}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {dados.slice(0, 10).map((row, i) => (
              <tr key={i}>
                {(Array.isArray(row) ? row : [row]).map((cell, j) => (
                  <td key={j}>{typeof cell === 'number' ? cell.toFixed(3) : String(cell)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}