import AlertaCard from '../components/AlertaCard'

const ALERTAS_CONFIG = [
  { key: 'atraso',        label: 'Atraso Crítico',               endpoint: '/alerts/atraso',                    cols: ['Data','Hora','Prob. Atraso','Risco'] },
  { key: 'comportamento', label: 'Comportamento Motorista',      endpoint: '/alerts/comportamento',             cols: ['Data','Hora','Score Comportamento'] },
  { key: 'fadiga',        label: 'Fadiga Crítica',               endpoint: '/alerts/fadiga_critica',            cols: ['Score Fadiga'] },
  { key: 'risco_rota',    label: 'Risco de Rota',                endpoint: '/alerts/risco_rota',                cols: ['Nível de Risco'] },
  { key: 'porto',         label: 'Porto Congestionado',          endpoint: '/alerts/porto_congestionado',       cols: ['Nível Congestionamento'] },
  { key: 'estoque',       label: 'Estoque Baixo',                endpoint: '/alerts/estoque_baixo',             cols: ['Nível de Estoque'] },
  { key: 'temperatura',   label: 'Temperatura da Carga',         endpoint: '/alerts/temperatura_da_carga',      cols: ['Temperatura IoT'] },
  { key: 'equipamentos',  label: 'Equipamentos Indisponíveis',   endpoint: '/alerts/equipamentos_indisponiveis', cols: ['Disponibilidade'] },
]

export default function Alertas() {
  return (
    <div>
      <div className="page-header">
        <div className="page-title">// ALERTAS</div>
        <div className="page-sub">Monitoramento de indicadores críticos em tempo real</div>
      </div>
      {ALERTAS_CONFIG.map(cfg => (
        <AlertaCard key={cfg.key} config={cfg} />
      ))}
    </div>
  )
}