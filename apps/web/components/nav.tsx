import Link from "next/link"

const links = [
  ["Dashboard", "/dashboard"],
  ["Pricing", "/pricing"],
  ["Inventory", "/inventory"],
  ["Orders", "/orders"],
  ["Settings", "/settings"],
  ["Reports", "/reports"]
]

export function TopNav() {
  return (
    <nav className="nav">
      <strong>CalcSteam Admin</strong>
      {links.map(([label, href]) => (
        <Link key={href} href={href}>{label}</Link>
      ))}
      <span style={{ marginLeft: "auto", opacity: 0.8 }}>role: operator</span>
    </nav>
  )
}
