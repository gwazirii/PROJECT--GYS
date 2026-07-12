export default function SectionHeader({ eyebrow, title, subtitle, center = false }) {
  return (
    <div className={center ? 'text-center' : ''}>
      {eyebrow && (
        <span className="inline-block text-primary-600 font-semibold text-sm uppercase tracking-widest mb-2">
          {eyebrow}
        </span>
      )}
      <h2 className="section-title">{title}</h2>
      {subtitle && (
        <p className={`section-subtitle ${center ? 'mx-auto' : ''}`}>{subtitle}</p>
      )}
    </div>
  )
}
