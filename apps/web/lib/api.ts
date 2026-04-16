export type OrderItem = { id: number; status: string; external_order_id: string }
export type PricingItem = { currency: string; nominal: number; recommended_price_rub?: number; status?: string }
export type InventoryItem = { id: number; masked_code: string; status: string; cost_rub: number }

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1"

async function getJson(path: string, token?: string) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store"
  })

  if (!res.ok) {
    throw new Error(`${path} fetch failed: ${res.status}`)
  }
  return res.json()
}

export async function loginRequest(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })

  if (!res.ok) {
    throw new Error(`login failed: ${res.status}`)
  }

  return res.json()
}

export async function fetchOrders(token?: string): Promise<OrderItem[]> {
  const data = await getJson("/orders", token)
  return data.items ?? []
}

export async function fetchPricing(token?: string): Promise<PricingItem[]> {
  const data = await getJson("/pricing/recommendations", token)
  return data.items ?? []
}

export async function fetchInventory(token?: string): Promise<InventoryItem[]> {
  const data = await getJson("/inventory/codes", token)
  return data
}
