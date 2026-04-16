import { StatusBadge } from "../../components/status-badge"
import { pricingRows } from "../../lib/mock"

export default function PricingPage() {
  return (
    <div className="grid">
      <h1>Pricing Matrix</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Currency</th>
              <th>Nominal</th>
              <th>Recommended price (RUB)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {pricingRows.map((row) => (
              <tr key={`${row.currency}-${row.nominal}`}>
                <td>{row.currency}</td>
                <td>{row.nominal}</td>
                <td>{row.recommendedPrice}</td>
                <td><StatusBadge status={row.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
