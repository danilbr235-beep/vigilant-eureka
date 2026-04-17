"use client"

import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { completeOrder, createOrder, fetchOrders, fulfillOrder, markOrderProblem, reserveOrder } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function OrdersPage() {
  const token = useAppStore((s) => s.token)
  const role = useAppStore((s) => s.role)
  const [reserveCodeId, setReserveCodeId] = useState<Record<number, string>>({})

  const [externalOrderId, setExternalOrderId] = useState("")
  const [currency, setCurrency] = useState("EUR")
  const [nominal, setNominal] = useState("20")

  const qc = useQueryClient()

  const ordersQuery = useQuery({
    queryKey: ["orders", token],
    queryFn: () => fetchOrders(token),
    retry: false
  })

  const createMutation = useMutation({
    mutationFn: () => createOrder(
      {
        external_order_id: externalOrderId,
        sell_nominal_id: 1,
        customer_currency: currency,
        customer_nominal: Number(nominal)
      },
      token
    ),
    onSuccess: () => {
      setExternalOrderId("")
      qc.invalidateQueries({ queryKey: ["orders", token] })
    }
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

  const completeMutation = useMutation({
    mutationFn: (orderId: number) => completeOrder(orderId, token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", token] })
  })

  const canOperate = role === "admin" || role === "operator"
  const canFulfillOrder = (status: string) => status === "reserved"
  const canCompleteOrder = (status: string) => status === "fulfilled" || status === "problem"

  return (
    <div className="grid">
      <h1>Orders</h1>

      <div className="card grid">
        <h3>Create order</h3>
        <input className="input" placeholder="External order id" value={externalOrderId} onChange={(e) => setExternalOrderId(e.target.value)} />
        <select className="select" value={currency} onChange={(e) => setCurrency(e.target.value)}>
          <option>EUR</option>
          <option>USD</option>
          <option>CNY</option>
          <option>KZT</option>
        </select>
        <input className="input" placeholder="Nominal" value={nominal} onChange={(e) => setNominal(e.target.value)} />
        <button className="button" disabled={!canOperate || createMutation.isPending} onClick={() => createMutation.mutate()}>Create</button>
      </div>

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
                    <button
                      className="button"
                      disabled={!canOperate || fulfillMutation.isPending || !canFulfillOrder(order.status)}
                      onClick={() => fulfillMutation.mutate(order.id)}
                    >
                      Fulfill
                    </button>{" "}
                    <button className="button" disabled={!canOperate || problemMutation.isPending} onClick={() => problemMutation.mutate(order.id)}>Problem</button>{" "}
                    <button
                      className="button"
                      disabled={!canOperate || completeMutation.isPending || !canCompleteOrder(order.status)}
                      onClick={() => completeMutation.mutate(order.id)}
                    >
                      Complete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        {createMutation.isError && <p>Failed to create order.</p>}
        {reserveMutation.isError && <p>Failed to reserve code for order.</p>}
        {fulfillMutation.isError && <p>Failed to fulfill order (only reserved orders can be fulfilled).</p>}
        {problemMutation.isError && <p>Failed to mark order as problem.</p>}
        {completeMutation.isError && <p>Failed to complete order (only fulfilled/problem orders can be completed).</p>}
      </div>
    </div>
  )
}
