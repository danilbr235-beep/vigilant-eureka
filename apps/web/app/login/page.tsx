export default function LoginPage() {
  return (
    <div className="card" style={{ maxWidth: 420, margin: "40px auto" }}>
      <h2>Login</h2>
      <div className="grid">
        <input className="input" placeholder="Email" />
        <input className="input" type="password" placeholder="Password" />
        <button className="button">Sign in</button>
      </div>
    </div>
  )
}
