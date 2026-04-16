export default function SettingsPage() {
  return (
    <div className="grid">
      <h1>Settings</h1>
      <div className="card grid">
        <label>Marketplace fee %</label>
        <input className="input" defaultValue="10" />
        <label>Risk reserve %</label>
        <input className="input" defaultValue="3" />
        <label>Default ad cost (RUB)</label>
        <input className="input" defaultValue="30" />
        <button className="button">Save</button>
      </div>
    </div>
  )
}
