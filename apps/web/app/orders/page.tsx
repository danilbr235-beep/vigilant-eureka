"use client"

import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { fetchOrders, fulfillOrder, markOrderProblem, reserveOrder } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function OrdersPage() {
  const token = useAppStore((s) => s.token)
  const role = useAppStore((s) => s.role)
  const [reserveCodeId, setReserveCodeId] = useState<Record<number, string>>({})
  const qc = useQueryClient()

  const ordersQuery = useQuery({
    queryKey: ["orders", token],
    queryFn: () => fetchOrders(token),
    retry: false
  })

  const reserveMutation = useMutation({
    mutationFn: ({ orderId, codeId }: { orderId: number; codeId: number }) => reserveOrder(orderId, [codeId], token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", token] })
  })

  const fulfillMutation = useMutation({
    mutationFn: (orderId: number) => fulfillOrder(orderId, token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", token] })
  })

  const problemMutation = useMutation({
    mutationFn: (orderId: number) => markOrderProblem(orderId, token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", token] })
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
                <th>Reserve code id</th>
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
                    <input
                      className="input"
                      style={{ width: 100 }}
                      value={reserveCodeId[order.id] ?? ""}
                      onChange={(e) => setReserveCodeId((prev) => ({ ...prev, [order.id]: e.target.value }))}
                      placeholder="code id"
                    />
                  </td>
                  <td>
                    <button
                      className="button"
                      disabled={!canOperate || reserveMutation.isPending}
                      onClick={() => {
                        const codeId = Number(reserveCodeId[order.id])
                        if (!codeId) return alert("Enter code id")
                        reserveMutation.mutate({ orderId: order.id, codeId })
                      }}
                    >
                      Reserve
                    </button>{" "}
                    <button className="button" disabled={!canOperate || fulfillMutation.isPending} onClick={() => fulfillMutation.mutate(order.id)}>Fulfill</button>{" "}
                    <button className="button" disabled={!canOperate || problemMutation.isPending} onClick={() => problemMutation.mutate(order.id)}>Problem</button>
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
