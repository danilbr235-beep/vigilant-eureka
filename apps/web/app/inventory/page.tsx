import { inventory } from "../../lib/mock"

export default function InventoryPage() {
  return (
    <div className="grid">
      <h1>Inventory</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Masked code</th>
              <th>Currency</th>
              <th>Nominal</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {inventory.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.masked}</td>
                <td>{item.currency}</td>
                <td>{item.nominal}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
