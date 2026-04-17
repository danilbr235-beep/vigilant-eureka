export type RiskStatus = "ok" | "low_margin" | "loss" | "no_combo" | "stale_rate" | "low_stock" | "manual_review"

export function StatusBadge({ status }: { status: RiskStatus }) {
  return <span className={`badge ${status}`}>{status}</span>
}
