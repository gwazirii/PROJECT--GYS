import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Users, CheckCircle } from 'lucide-react'
import PageHero from '../components/ui/PageHero'
import SectionHeader from '../components/ui/SectionHeader'

const categories = ['All', 'Education', 'Health', 'Agriculture', 'Youth', 'Women']

const programs = [
  {
    id: 1,
    category: 'Education',
    emoji: '🎓',
    title: 'Scholarship Fund',
    desc: 'Full and partial scholarships for students from low-income families at secondary and tertiary levels.',
    beneficiaries: 3200,
    status: 'Active',
    budget: 'GHS 1.2M',
    outcomes: ['3,200 scholarships awarded', '92% retention rate', '78% graduate employment'],
  },
  {
    id: 2,
    category: 'Health',
    emoji: '🏥',
    title: 'Mobile Health Clinics',
    desc: 'Free medical services delivered to remote communities through mobile units equipped for general practice and maternal care.',
    beneficiaries: 8500,
    status: 'Active',
    budget: 'GHS 980K',
    outcomes: ['8,500+ consultations', '42 communities reached', '60% reduction in untreated cases'],
  },
  {
    id: 3,
    category: 'Agriculture',
    emoji: '🌱',
    title: 'Farmer Training Initiative',
    desc: 'Modern farming techniques, irrigation training, and market linkage support for smallholder farmers.',
    beneficiaries: 1800,
    status: 'Active',
    budget: 'GHS 650K',
    outcomes: ['1,800 farmers trained', '35% yield increase', '200 cooperatives formed'],
  },
  {
    id: 4,
    category: 'Youth',
    emoji: '💡',
    title: 'Youth Skills Centre',
    desc: 'Vocational training in technology, trades, and entrepreneurship with job placement support.',
    beneficiaries: 2100,
    status: 'Active',
    budget: 'GHS 750K',
    outcomes: ['2,100 youth trained', '70% placed in jobs', '320 businesses started'],
  },
  {
    id: 5,
    category: 'Women',
    emoji: '👩‍💼',
    title: "Women's Empowerment Program",
    desc: 'Financial literacy, micro-grants, and leadership training for women entrepreneurs.',
    beneficiaries: 950,
    status: 'Active',
    budget: 'GHS 420K',
    outcomes: ['950 women supported', 'GHS 2.4M in micro-grants', '85% business survival rate'],
  },
  {
    id: 6,
    category: 'Education',
    emoji: '📚',
    title: 'School Library Project',
    desc: 'Building and stocking libraries in rural schools to promote literacy and a love of reading.',
    beneficiaries: 5600,
    status: 'Active',
    budget: 'GHS 330K',
    outcomes: ['28 libraries built', '5,600 students access', '40% literacy improvement'],
  },
]

const statusColor = {
  Active:    'bg-primary-100 text-primary-700',
  Completed: 'bg-gray-100 text-gray-600',
  Planning:  'bg-gold-100 text-gold-700',
}

export default function Programs() {
  const [active, setActive] = useState('All')

  const filtered = active === 'All'
    ? programs
    : programs.filter((p) => p.category === active)

  return (
    <>
      <PageHero
        title="Our Programs"
        subtitle="Every program is designed with clear objectives, measurable outcomes, and full community involvement."
      />

      {/* Filter */}
      <section className="py-8 bg-white border-b sticky top-[calc(4rem+1.75rem)] z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap gap-2">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActive(cat)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-colors ${
                active === cat
                  ? 'bg-primary-700 text-white shadow'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </section>

      {/* Program cards */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
            {filtered.map((p) => (
              <div key={p.id} className="card flex flex-col">
                {/* Card header */}
                <div className="bg-gray-900 p-6 flex items-start justify-between">
                  <span className="text-4xl">{p.emoji}</span>
                  <span className={`badge text-xs ${statusColor[p.status]}`}>{p.status}</span>
                </div>

                {/* Content */}
                <div className="p-6 flex flex-col flex-1">
                  <span className="text-xs font-semibold text-primary-600 uppercase tracking-wider mb-1">
                    {p.category}
                  </span>
                  <h3 className="font-heading font-bold text-xl text-gray-900 mb-2">{p.title}</h3>
                  <p className="text-gray-500 text-sm leading-relaxed mb-4 flex-1">{p.desc}</p>

                  {/* Meta */}
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4 border-t pt-4">
                    <span className="flex items-center gap-1.5">
                      <Users size={14} className="text-primary-500" />
                      {p.beneficiaries.toLocaleString()} beneficiaries
                    </span>
                    <span className="font-medium text-gray-700">Budget: {p.budget}</span>
                  </div>

                  {/* Outcomes */}
                  <ul className="space-y-1.5">
                    {p.outcomes.map((o) => (
                      <li key={o} className="flex items-center gap-2 text-xs text-gray-600">
                        <CheckCircle size={13} className="text-primary-500 shrink-0" />
                        {o}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Impact summary */}
      <section className="py-16 bg-primary-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Collective Impact"
            title="Numbers That Matter"
            center
          />
          <div className="mt-10 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            {[
              { v: '47',   l: 'Active Programs' },
              { v: '12K+', l: 'Lives Impacted' },
              { v: '8',    l: 'Regions Covered' },
              { v: '15+',  l: 'Years of Service' },
            ].map(({ v, l }) => (
              <div key={l}>
                <p className="font-heading font-extrabold text-4xl text-gold-400">{v}</p>
                <p className="text-primary-100 text-sm mt-1">{l}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-white text-center">
        <h2 className="font-heading font-bold text-2xl text-gray-900 mb-4">
          Want to Support a Program?
        </h2>
        <p className="text-gray-500 max-w-xl mx-auto mb-7">
          Your donation goes directly to programs. View our financial reports to see exactly how funds are used.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/donate" className="btn-gold">Donate Now <ArrowRight size={16} /></Link>
          <Link to="/reports" className="btn-outline">View Reports</Link>
        </div>
      </section>
    </>
  )
}
