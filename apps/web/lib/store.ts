"use client"

import { create } from "zustand"

export type Role = "admin" | "operator" | "viewer"

type AppState = {
  token: string
  role: Role
  setToken: (token: string) => void
  setRole: (role: Role) => void
}

export const useAppStore = create<AppState>((set) => ({
  token: "",
  role: "operator",
  setToken: (token) => set({ token }),
  setRole: (role) => set({ role })
}))
