"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"

import { useAppStore } from "../../lib/store"
import { loginRequest } from "../../lib/api"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const setToken = useAppStore((s) => s.setToken)
  const setRole = useAppStore((s) => s.setRole)
  const router = useRouter()

  async function onSubmit() {
    try {
      const data = await loginRequest(email, password)
      setToken(data.access_token)
      setRole(data.role)
      router.push("/orders")
    } catch {
      alert("Login failed")
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420, margin: "40px auto" }}>
      <h2>Login</h2>
      <div className="grid">
        <input className="input" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="input" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="button" onClick={onSubmit}>Sign in</button>
      </div>
    </div>
  )
}
