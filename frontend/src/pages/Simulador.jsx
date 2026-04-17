import { useState } from 'react'
import axios from 'axios'
import KpiCard from '../components/KpiCard'

const API = 'http://localhost:8000'

const CAMPOS = [
  { key: 'delay_probability',         label: 'Probabilidade de Atraso',   min: 0,   max: 1,    step: 0.01, hint: '0.0 = sem risco  /  1.0 = certeza de atraso' },
  { key: 'driver_behavior_score',     label: 'Score do Motorista',         min: 0,   max: 1,    step: 0.01, hint: '0.0 = péssimo  /  1.0 = excelente' },
  { key: 'fatigue_monitoring_score',  label: 'Score de Fadiga',            min: 0,   max: 1,    step: 0.01, hint: '0.0 = descansado  /  1.0 = fadigado' },
  { key: 'route_risk_level',          label: 'Nível de Risco da Rota',     min: 0,   max: 10,   step: 0.1,  hint: '0 = segura  /  10 = crítica' },
  { key: 'port_congestion_level',     label: 'Congestionamento Portuário', min: 0,   max: 10,   step: 0.1,  hint: '0 = livre  /  10 = congestionado' },
  { key: 'warehouse_inventory_level', label: 'Nível de Estoque',           min: 0,   max: 1000, step: 1,    hint: 'unidades disponíveis no armazém' },
  { key: 'iot_temperature',           label: 'Temperatura da Carga (°C)',  min: -10, max: 40,   step: 0.5,  hint: 'temperatura medida pelo sensor IoT' },
  { key: 'shipping_costs',            label: 'Custo de Frete (R$)',         min: 100, max: 1000, step: 1,    hint: 'custo estimado de envio' },
]

const DEFAULTS = {
  delay_probability: 0.5,
  driver_behavior_score: 0.5,
  fatigue_monitoring_score: 0.6,
  route_risk_level: 5,
  port_congestion_level: 5,
  warehouse_inventory_level: 300,
  iot_temperature: 10,
  shipping_costs: 450,
}

export default function Simulador() {
  const [form, setForm]       = useState(DEFAULTS)
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [erro, setErro]       = useState(null)

  const handleChange = (key, val) => setForm(f => ({ ...f, [key]: parseFloat(val) }))

  const handleSubmit = async () => {
    setLoading(true)
    setErro(null)
    setResult(null)
    try {
      const r = await axios.post(`${API}/inserir/registro`, form)
      setResult(r.data)
    } catch {
      setErro('Erro ao conectar com a API. Verifique se o servidor está rodando.')
    } finally {
      setLoading(false)
    }
  }

  const riskColor = (r) =>
    r === 'High_Risk'     ? 'var(--danger)' :
    r === 'Moderate_Risk' ? 'var(--warn)'   : 'var(--ok)'

  return (
    <div>
      <div className="page-header">
        <div className="page-title">// SIMULADOR</div>
        <div className="page-sub">Simule uma operação e veja os alertas disparados em tempo real</div>
      </div>

      <div className="table-wrap" style={{ padding: '24px', marginBottom: '24px' }}>
        <div className="form-grid">
          {CAMPOS.map(c => (
            <div className="form-group" key={c.key}>
              <label className="form-label">{c.label}</label>
              <input
                className="form-input"
                type="number"
                min={c.min}
                max={c.max}
                step={c.step}
                value={form[c.key]}
                onChange={e => handleChange(c.key, e.target.value)}
              />
              <span className="form-hint">{c.hint}</span>
            </div>
          ))}
        </div>
        <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Simulando...' : '→ Simular Operação'}
        </button>
      </div>

      {erro && (
        <div className="result-box" style={{ borderColor: 'var(--danger)' }}>
          <div style={{ color: 'var(--danger)', fontFamily: 'var(--font-mono)', fontSize: '13px' }}>{erro}</div>
        </div>
      )}

      {result && (
        <div className="result-box">
          <div style={{ fontSize: '11px', color: 'var(--muted)', marginBottom: '8px', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Resultado da Simulação
          </div>

          <div className="cards-grid" style={{ marginBottom: '20px' }}>
            <KpiCard
              label="Classificação de Risco"
              value={result.risk_classification}
              sub={`${result.data} às ${result.hora}`}
              variant={result.risk_classification === 'High_Risk' ? 'danger' : result.risk_classification === 'Moderate_Risk' ? 'warn' : 'ok'}
            />
            <KpiCard
              label="Alertas Disparados"
              value={result.alertas_disparados[0] === 'Nenhum alerta' ? '0' : result.alertas_disparados.length}
              sub={result.alertas_disparados[0] === 'Nenhum alerta' ? 'operação normal' : 'requer atenção'}
              variant={result.alertas_disparados[0] === 'Nenhum alerta' ? 'ok' : 'danger'}
            />
          </div>

          <div style={{ fontSize: '11px', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '10px' }}>
            Detalhes dos Alertas
          </div>
          <div className="alert-list">
            {result.alertas_disparados.map((a, i) => (
              <div key={i} className={`alert-item ${a === 'Nenhum alerta' ? 'ok' : 'danger'}`}>
                <span>{a === 'Nenhum alerta' ? '✓' : '⚠'}</span>
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}