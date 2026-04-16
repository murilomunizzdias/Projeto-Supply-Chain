export default function KpiCard({ label, value, sub, variant }) {
  return (
    <div className="card">
      <div className="card-label">{label}</div>
      <div className={`card-value ${variant ?? ''}`}>{value}</div>
      {sub && <div className="card-sub">{sub}</div>}
    </div>
  )
}