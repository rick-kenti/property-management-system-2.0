export default function StatCard({ title, value, subtitle, accent }) {
  return (
    <div className={`stat-card accent-${accent}`}>
      <p className="stat-title">{title}</p>
      <h2 className="stat-value">{value}</h2>
      {subtitle && <p className="stat-subtitle">{subtitle}</p>}
    </div>
  );
}
