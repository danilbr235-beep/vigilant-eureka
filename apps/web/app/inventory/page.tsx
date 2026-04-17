"use client"

import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { createCode, fetchInventory, patchCodeStatus, revealCode } from "../../lib/api"
import { inventory as mockInventory } from "../../lib/mock"
import { useAppStore } from "../../lib/store"

export default function InventoryPage() {
  const token = useAppStore((s) => s.token)
  const role = useAppStore((s) => s.role)
  const [revealed, setRevealed] = useState<Record<number, string>>({})

  const [rawCode, setRawCode] = useState("")
  const [costRub, setCostRub] = useState("100")

  const qc = useQueryClient()

  const query = useQuery({
    queryKey: ["inventory", token],
    queryFn: () => fetchInventory(token),
    retry: false
  })

  const createMutation = useMutation({
    mutationFn: () => createCode(
      {
        supplier_code_type_id: 1,
        purchase_batch_id: 1,
        code: rawCode,
        cost_rub: Number(costRub)
      },
      token
    ),
    onSuccess: () => {
      setRawCode("")
      qc.invalidateQueries({ queryKey: ["inventory", token] })
    }
  })

  const revealMutation = useMutation({
    mutationFn: (codeId: number) => revealCode(codeId, token),
    onSuccess: (data) => {
      if (data?.id && data?.code) {
        setRevealed((prev) => ({ ...prev, [data.id as number]: String(data.code) }))
      }
    }
  })

  const statusMutation = useMutation({
    mutationFn: ({ codeId, status }: { codeId: number; status: string }) => patchCodeStatus(codeId, status, token),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["inventory", token] })
  })

  const rows = query.data && query.data.length > 0
    ? query.data.map((item) => ({
      id: item.id,
      masked: item.masked_code,
      status: item.status
    }))
    : mockInventory.map((m) => ({ id: m.id, masked: m.masked, status: m.status }))

  const canReveal = role === "admin" || role === "operator"

  return (
    <div className="grid">
      <h1>Inventory</h1>

      <div className="card grid">
        <h3>Create code</h3>
        <input className="input" value={rawCode} onChange={(e) => setRawCode(e.target.value)} placeholder="AAAA-BBBB-CCCC" />
        <input className="input" value={costRub} onChange={(e) => setCostRub(e.target.value)} placeholder="Cost RUB" />
        <button className="button" disabled={!canReveal || createMutation.isPending} onClick={() => createMutation.mutate()}>
          Add code
        </button>
      </div>

      <div className="card">
        {query.isError && <p>API unavailable, showing mock inventory.</p>}
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Masked code</th>
              <th>Revealed code</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.masked}</td>
                <td>{revealed[item.id] ?? "—"}</td>
                <td>{item.status}</td>
                <td>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button
                      className="button"
                      disabled={!canReveal || revealMutation.isPending}
                      onClick={() => revealMutation.mutate(item.id)}
                    >
                      Reveal
                    </button>
                    <select
                      className="select"
                      defaultValue={item.status}
                      disabled={!canReveal || statusMutation.isPending}
                      onChange={(e) => statusMutation.mutate({ codeId: item.id, status: e.target.value })}
                    >
                      <option value="available">available</option>
                      <option value="reserved">reserved</option>
                      <option value="sold">sold</option>
                      <option value="blocked">blocked</option>
                    </select>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
