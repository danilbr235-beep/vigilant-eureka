"use client"

import { useQuery } from "@tanstack/react-query"

import { fetchInventory } from "../../lib/api"
import { inventory as mockInventory } from "../../lib/mock"
import { useAppStore } from "../../lib/store"

export default function InventoryPage() {
  const token = useAppStore((s) => s.token)
  const query = useQuery({
    queryKey: ["inventory", token],
    queryFn: () => fetchInventory(token),
    retry: false
  })

  const rows = query.data && query.data.length > 0
    ? query.data.map((item) => ({
      id: item.id,
      masked: item.masked_code,
      currency: "N/A",
      nominal: "N/A",
      status: item.status
    }))
    : mockInventory

  return (
    <div className="grid">
      <h1>Inventory</h1>
      <div className="card">
        {query.isError && <p>API unavailable, showing mock inventory.</p>}
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
            {rows.map((item) => (
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
