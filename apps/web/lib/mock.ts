import type { RiskStatus } from "../components/status-badge"

export const pricingRows: Array<{ currency: string; nominal: number; recommendedPrice: number; status: RiskStatus }> = [
  { currency: "EUR", nominal: 20, recommendedPrice: 2290, status: "ok" },
  { currency: "USD", nominal: 50, recommendedPrice: 5190, status: "low_margin" },
  { currency: "CNY", nominal: 200, recommendedPrice: 2590, status: "manual_review" }
]

export const orders = [
  { id: 101, nominal: "EUR 20", status: "reserved" },
  { id: 102, nominal: "USD 50", status: "new" },
  { id: 103, nominal: "CNY 200", status: "problem" }
]

export const inventory = [
  { id: 1, masked: "****1234", status: "new", currency: "SGD", nominal: 20 },
  { id: 2, masked: "****7822", status: "reserved", currency: "MYR", nominal: 10 },
  { id: 3, masked: "****9921", status: "new", currency: "SGD", nominal: 50 }
]
