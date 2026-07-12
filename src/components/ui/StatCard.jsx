export default function StatCard({ value, label, icon: Icon, color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-50 text-primary-700',
    gold:    'bg-gold-50 text-gold-700',
    black:   'bg-gray-100 text-gray-800',
  }

  return (
    <div className="card p-6 flex flex-col items-center text-center gap-3">
      {Icon && (
        <span className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl ${colors[color]}`}>
          <Icon size={28} />
        </span>
      )}
      <span className="font-heading font-extrabold text-4xl text-gray-900">{value}</span>
      <span className="text-gray-500 text-sm font-medium">{label}</span>
    </div>
  )
}
