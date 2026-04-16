"use client"

import Link from "next/link"

import { type Role, useAppStore } from "../lib/store"

const links = [
  ["Dashboard", "/dashboard"],
  ["Pricing", "/pricing"],
  ["Inventory", "/inventory"],
  ["Orders", "/orders"],
  ["Settings", "/settings"],
  ["Reports", "/reports"]
]

const roles: Role[] = ["admin", "operator", "viewer"]

export function TopNav() {
  const role = useAppStore((s) => s.role)
  const setRole = useAppStore((s) => s.setRole)

  return (
    <nav className="nav">
      <strong>CalcSteam Admin</strong>
      {links.map(([label, href]) => (
        <Link key={href} href={href}>{label}</Link>
      ))}
      <select className="select" value={role} onChange={(e) => setRole(e.target.value as Role)} style={{ marginLeft: "auto" }}>
        {roles.map((r) => <option key={r} value={r}>{r}</option>)}
      </select>
    </nav>
  )
}
