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

async function postJson(path: string, body: unknown, token?: string, extraHeaders?: Record<string, string>) {
  const headers: Record<string, string> = { "Content-Type": "application/json", ...(extraHeaders ?? {}) }
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body)
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${path} failed: ${res.status} ${text}`)
  }

  return res.json()
}

export async function loginRequest(email: string, password: string) {
  return postJson("/auth/login", { email, password })
}

export async function fetchOrders(token?: string): Promise<OrderItem[]> {
  const data = await getJson("/orders", token)
  return data.items ?? []
}

export async function reserveOrder(orderId: number, codeIds: number[], token?: string) {
  return postJson(
    `/orders/${orderId}/reserve`,
    { code_item_ids: codeIds },
    token,
    { "X-Idempotency-Key": crypto.randomUUID() }
  )
}

export async function fulfillOrder(orderId: number, token?: string) {
  return postJson(`/orders/${orderId}/fulfill`, {}, token)
}

export async function markOrderProblem(orderId: number, token?: string) {
  return postJson(`/orders/${orderId}/problem`, {}, token)
}

export async function fetchPricing(token?: string): Promise<PricingItem[]> {
  const data = await getJson("/pricing/recommendations", token)
  return data.items ?? []
}

export async function fetchInventory(token?: string): Promise<InventoryItem[]> {
  return getJson("/inventory/codes", token)
}

export async function revealCode(codeId: number, token?: string) {
  return getJson(`/inventory/codes/${codeId}/reveal`, token)
}
