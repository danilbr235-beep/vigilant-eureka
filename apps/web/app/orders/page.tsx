import { orders } from "../../lib/mock"

export default function OrdersPage() {
  return (
    <div className="grid">
      <h1>Orders</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Nominal</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.nominal}</td>
                <td>{order.status}</td>
                <td>
                  <button className="button">Reserve</button>{" "}
                  <button className="button">Fulfill</button>{" "}
                  <button className="button">Problem</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
