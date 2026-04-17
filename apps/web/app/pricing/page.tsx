"use client"

import { useQuery } from "@tanstack/react-query"

import { StatusBadge, type RiskStatus } from "../../components/status-badge"
import { fetchPricing } from "../../lib/api"
import { pricingRows } from "../../lib/mock"
import { useAppStore } from "../../lib/store"

const allowedStatuses: RiskStatus[] = ["ok", "low_margin", "loss", "no_combo", "stale_rate", "low_stock", "manual_review"]

export default function PricingPage() {
  const token = useAppStore((s) => s.token)
  const query = useQuery({
    queryKey: ["pricing", token],
    queryFn: () => fetchPricing(token),
    retry: false
  })

  const rows = query.data && query.data.length > 0
    ? query.data.map((row) => ({
      currency: row.currency,
      nominal: row.nominal,
      recommendedPrice: row.recommended_price_rub ?? 0,
      status: allowedStatuses.includes((row.status as RiskStatus) || "ok") ? (row.status as RiskStatus) : "ok"
    }))
    : pricingRows

  return (
    <div className="grid">
      <h1>Pricing Matrix</h1>
      <div className="card">
        {query.isError && <p>API unavailable, showing mock rows.</p>}
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
            {rows.map((row) => (
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
