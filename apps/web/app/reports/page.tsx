"use client"

import { useQuery } from "@tanstack/react-query"

import { fetchReportAudit, fetchReportOrders, fetchReportProblems, fetchReportProfit } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function ReportsPage() {
  const token = useAppStore((s) => s.token)

  const profitQ = useQuery({ queryKey: ["report-profit", token], queryFn: () => fetchReportProfit(token), retry: false })
  const ordersQ = useQuery({ queryKey: ["report-orders", token], queryFn: () => fetchReportOrders(token), retry: false })
  const problemsQ = useQuery({ queryKey: ["report-problems", token], queryFn: () => fetchReportProblems(token), retry: false })
  const auditQ = useQuery({ queryKey: ["report-audit", token], queryFn: () => fetchReportAudit(token), retry: false })

  return (
    <div className="grid">
      <h1>Reports</h1>
      <div className="card">
        <strong>Profit (fulfilled nominal)</strong>
        <div>{String(profitQ.data?.gross_nominal_fulfilled ?? "—")}</div>
      </div>

      <div className="card">
        <strong>Orders by status</strong>
        <pre>{JSON.stringify(ordersQ.data?.orders ?? [], null, 2)}</pre>
      </div>

      <div className="card">
        <strong>Problem orders</strong>
        <pre>{JSON.stringify(problemsQ.data?.items ?? [], null, 2)}</pre>
      </div>

      <div className="card">
        <strong>Audit log (last)</strong>
        <pre>{JSON.stringify(auditQ.data?.items ?? [], null, 2)}</pre>
      </div>
    </div>
  )
}
