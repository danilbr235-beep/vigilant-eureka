export type OrderItem = { id: number; status: string; external_order_id: string }

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1"

export async function fetchOrders(token?: string): Promise<OrderItem[]> {
  const res = await fetch(`${API_BASE}/orders`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store"
  })

  if (!res.ok) {
    throw new Error(`orders fetch failed: ${res.status}`)
  }

  const data = await res.json()
  return data.items ?? []
}
