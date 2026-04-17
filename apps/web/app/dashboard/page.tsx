"use client"

import { useQuery } from "@tanstack/react-query"

import { fetchDashboardSummary } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function DashboardPage() {
  const token = useAppStore((s) => s.token)
  const q = useQuery({
    queryKey: ["dashboard-summary", token],
    queryFn: () => fetchDashboardSummary(token),
    retry: false
  })

  const total = Number(q.data?.total_orders ?? 0)
  const fulfilled = Number(q.data?.fulfilled_orders ?? 0)
  const problems = Number(q.data?.problem_orders ?? 0)

  return (
    <div className="grid">
      <h1>Dashboard</h1>
      <div className="grid grid-3">
        <div className="card"><strong>Total orders</strong><div>{total}</div></div>
        <div className="card"><strong>Fulfilled</strong><div>{fulfilled}</div></div>
        <div className="card"><strong>Problems</strong><div>{problems}</div></div>
      </div>
      {q.isError && <div className="card">Could not load dashboard summary from API.</div>}
    </div>
  )
}
