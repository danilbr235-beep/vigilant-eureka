export default function DashboardPage() {
  return (
    <div className="grid">
      <h1>Dashboard</h1>
      <div className="grid grid-3">
        <div className="card"><strong>Profit today</strong><div>₽ 12,340</div></div>
        <div className="card"><strong>Avg margin</strong><div>9.4%</div></div>
        <div className="card"><strong>Low stock</strong><div>7 SKUs</div></div>
      </div>
      <div className="card">
        <h3>Risk items</h3>
        <ul>
          <li>USD 50 — low_margin</li>
          <li>CNY 200 — manual_review</li>
        </ul>
      </div>
    </div>
  )
}
