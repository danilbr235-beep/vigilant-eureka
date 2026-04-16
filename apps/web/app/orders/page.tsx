"use client"

import { useQuery } from "@tanstack/react-query"

import { fetchOrders } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function OrdersPage() {
  const token = useAppStore((s) => s.token)
  const role = useAppStore((s) => s.role)

  const ordersQuery = useQuery({
    queryKey: ["orders", token],
    queryFn: () => fetchOrders(token),
    retry: false
  })

  const canOperate = role === "admin" || role === "operator"

  return (
    <div className="grid">
      <h1>Orders</h1>
      <div className="card">
        {ordersQuery.isLoading ? (
          <p>Loading…</p>
        ) : ordersQuery.isError ? (
          <p>Could not load from API, check backend auth/availability.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>External ID</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {ordersQuery.data?.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.external_order_id}</td>
                  <td>{order.status}</td>
                  <td>
                    <button className="button" disabled={!canOperate}>Reserve</button>{" "}
                    <button className="button" disabled={!canOperate}>Fulfill</button>{" "}
                    <button className="button" disabled={!canOperate}>Problem</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
