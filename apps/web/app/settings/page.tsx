"use client"

import { useState } from "react"
import { useMutation } from "@tanstack/react-query"

import { patchPricingSettings } from "../../lib/api"
import { useAppStore } from "../../lib/store"

export default function SettingsPage() {
  const token = useAppStore((s) => s.token)
  const role = useAppStore((s) => s.role)

  const [marketplaceFee, setMarketplaceFee] = useState("10")
  const [riskReserve, setRiskReserve] = useState("3")
  const [adCost, setAdCost] = useState("30")

  const canSave = role === "admin"

  const saveMutation = useMutation({
    mutationFn: () => patchPricingSettings({
      marketplace_fee_percent: Number(marketplaceFee),
      risk_reserve_percent: Number(riskReserve),
      default_ad_cost_per_sale: Number(adCost)
    }, token)
  })

  return (
    <div className="grid">
      <h1>Settings</h1>
      <div className="card grid">
        <label>Marketplace fee %</label>
        <input className="input" value={marketplaceFee} onChange={(e) => setMarketplaceFee(e.target.value)} />
        <label>Risk reserve %</label>
        <input className="input" value={riskReserve} onChange={(e) => setRiskReserve(e.target.value)} />
        <label>Default ad cost (RUB)</label>
        <input className="input" value={adCost} onChange={(e) => setAdCost(e.target.value)} />

        <button className="button" disabled={!canSave || saveMutation.isPending} onClick={() => saveMutation.mutate()}>
          Save
        </button>

        {saveMutation.isSuccess && <small>Saved.</small>}
        {saveMutation.isError && <small>Save failed.</small>}
      </div>
    </div>
  )
}
