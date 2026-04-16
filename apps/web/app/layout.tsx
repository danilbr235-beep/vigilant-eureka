import "./globals.css"
import { TopNav } from "../components/nav"
import { WebQueryProvider } from "../components/query-provider"

export const metadata = {
  title: "CalcSteam Admin"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <WebQueryProvider>
          <TopNav />
          <div className="container">{children}</div>
        </WebQueryProvider>
      </body>
    </html>
  )
}
