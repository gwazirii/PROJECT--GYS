export default function PageHero({ title, subtitle, bgClass = 'bg-gray-900' }) {
  return (
    <section className={`${bgClass} pt-32 pb-16 px-4`}>
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="font-heading font-extrabold text-4xl md:text-5xl text-white leading-tight">
          {title}
        </h1>
        {subtitle && (
          <p className="mt-4 text-lg text-gray-300 max-w-2xl mx-auto">{subtitle}</p>
        )}
        {/* Gold accent line */}
        <div className="mt-6 mx-auto w-20 h-1 bg-gold-500 rounded-full" />
      </div>
    </section>
  )
}
