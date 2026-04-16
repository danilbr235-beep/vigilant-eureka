import "./globals.css"
import { TopNav } from "../components/nav"

export const metadata = {
  title: "CalcSteam Admin"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <TopNav />
        <div className="container">{children}</div>
      </body>
    </html>
  )
}
