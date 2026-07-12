import { useState } from 'react'
import { FileText, Download, BarChart3, Shield, ExternalLink } from 'lucide-react'
import PageHero from '../components/ui/PageHero'
import SectionHeader from '../components/ui/SectionHeader'

const reports = [
  { year: 2024, type: 'Annual Report',    title: 'GYS Annual Report 2024',           size: '4.2 MB', pages: 68, status: 'Published' },
  { year: 2024, type: 'Financial Audit',  title: 'Audited Financial Statements 2024', size: '2.1 MB', pages: 32, status: 'Published' },
  { year: 2024, type: 'Impact Report',    title: 'Program Impact Report Q3 2024',     size: '3.5 MB', pages: 44, status: 'Published' },
  { year: 2023, type: 'Annual Report',    title: 'GYS Annual Report 2023',           size: '3.9 MB', pages: 65, status: 'Published' },
  { year: 2023, type: 'Financial Audit',  title: 'Audited Financial Statements 2023', size: '1.8 MB', pages: 30, status: 'Published' },
  { year: 2023, type: 'Impact Report',    title: 'Program Impact Report 2023',        size: '3.1 MB', pages: 40, status: 'Published' },
  { year: 2022, type: 'Annual Report',    title: 'GYS Annual Report 2022',           size: '3.4 MB', pages: 62, status: 'Published' },
  { year: 2022, type: 'Financial Audit',  title: 'Audited Financial Statements 2022', size: '1.7 MB', pages: 28, status: 'Published' },
]

const years = ['All', '2024', '2023', '2022']
const types = ['All', 'Annual Report', 'Financial Audit', 'Impact Report']

const typeIcon = {
  'Annual Report':   FileText,
  'Financial Audit': BarChart3,
  'Impact Report':   Shield,
}

const typeColor = {
  'Annual Report':   'bg-primary-100 text-primary-700',
  'Financial Audit': 'bg-gold-100 text-gold-700',
  'Impact Report':   'bg-gray-100 text-gray-700',
}

const budgetAllocation = [
  { label: 'Programs & Services',  pct: 72, color: 'bg-primary-600' },
  { label: 'Administration',       pct: 12, color: 'bg-gold-500' },
  { label: 'Fundraising',          pct: 8,  color: 'bg-primary-300' },
  { label: 'Research & Evaluation',pct: 8,  color: 'bg-gray-400' },
]

export default function Reports() {
  const [yearFilter, setYearFilter] = useState('All')
  const [typeFilter, setTypeFilter] = useState('All')

  const filtered = reports.filter((r) => {
    const yMatch = yearFilter === 'All' || r.year === parseInt(yearFilter)
    const tMatch = typeFilter === 'All' || r.type === typeFilter
    return yMatch && tMatch
  })

  return (
    <>
      <PageHero
        title="Transparency Reports"
        subtitle="Full access to our financial records, audit reports, and program impact data — because accountability starts with openness."
      />

      {/* Pledge strip */}
      <section className="bg-primary-700 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Shield size={28} className="text-gold-400 shrink-0" />
            <div>
              <p className="font-semibold text-white">Our Transparency Pledge</p>
              <p className="text-primary-100 text-sm">All reports are independently audited and published within 90 days of the reporting period.</p>
            </div>
          </div>
          <span className="badge bg-gold-500 text-black font-semibold text-sm px-4 py-2 shrink-0">
            Verified ✓
          </span>
        </div>
      </section>

      {/* Budget allocation visual */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Fund Allocation"
            title="Where Does Your Money Go?"
            subtitle="72 cents of every dollar goes directly to programs. Here's the full breakdown."
            center
          />
          <div className="mt-10 space-y-4">
            {budgetAllocation.map((item) => (
              <div key={item.label}>
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="font-medium text-gray-700">{item.label}</span>
                  <span className="font-bold text-gray-900">{item.pct}%</span>
                </div>
                <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${item.color} transition-all duration-700`}
                    style={{ width: `${item.pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Reports list */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader eyebrow="Document Library" title="Download Our Reports" center />

          {/* Filters */}
          <div className="mt-8 flex flex-wrap gap-6 justify-center">
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Year:</span>
              {years.map((y) => (
                <button
                  key={y}
                  onClick={() => setYearFilter(y)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    yearFilter === y ? 'bg-primary-700 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'
                  }`}
                >
                  {y}
                </button>
              ))}
            </div>
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Type:</span>
              {types.map((t) => (
                <button
                  key={t}
                  onClick={() => setTypeFilter(t)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    typeFilter === t ? 'bg-primary-700 text-white' : 'bg-white text-gray-600 border hover:bg-gray-50'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* Cards */}
          <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
            {filtered.map((r, i) => {
              const Icon = typeIcon[r.type] || FileText
              return (
                <div key={i} className="card p-6 flex items-start gap-5">
                  <div className="w-14 h-14 rounded-xl bg-gray-100 flex items-center justify-center shrink-0">
                    <Icon size={26} className="text-primary-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className={`badge text-xs ${typeColor[r.type]}`}>{r.type}</span>
                      <span className="text-xs text-gray-400">{r.year}</span>
                    </div>
                    <h4 className="font-semibold text-gray-900 truncate">{r.title}</h4>
                    <p className="text-xs text-gray-400 mt-0.5">{r.pages} pages · {r.size}</p>
                  </div>
                  <button
                    aria-label={`Download ${r.title}`}
                    className="shrink-0 w-10 h-10 rounded-lg bg-primary-50 hover:bg-primary-100 flex items-center justify-center text-primary-700 transition-colors"
                  >
                    <Download size={18} />
                  </button>
                </div>
              )
            })}
          </div>

          {filtered.length === 0 && (
            <p className="text-center text-gray-400 py-12">No reports match the selected filters.</p>
          )}
        </div>
      </section>

      {/* Third-party verification */}
      <section className="py-16 bg-gray-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="text-gold-400 font-semibold uppercase tracking-widest text-sm mb-3">Independent Verification</p>
          <h2 className="font-heading font-bold text-3xl text-white mb-4">
            Audited by Trusted Partners
          </h2>
          <p className="text-gray-400 mb-8">
            Our financial statements are independently audited annually by certified firms.
          </p>
          <div className="flex flex-wrap justify-center gap-8 text-gray-400 font-heading font-bold text-lg">
            {['Deloitte Ghana', 'KPMG Africa', 'PricewaterhouseCoopers'].map((f) => (
              <span key={f}>{f}</span>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
