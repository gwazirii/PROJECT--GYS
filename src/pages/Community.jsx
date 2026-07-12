import { Users, HandHeart, Sparkles, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'

const groups = [
  {
    title: 'Volunteer Network',
    description: 'Join weekly community service days and help deliver direct support in underserved areas.',
    icon: HandHeart,
  },
  {
    title: 'Youth Circle',
    description: 'Mentorship, leadership training, and entrepreneurship sessions for young changemakers.',
    icon: Sparkles,
  },
  {
    title: 'Partner Forums',
    description: 'Collaborate with civic leaders, local businesses, and donors to expand impact.',
    icon: Users,
  },
]

export default function Community() {
  return (
    <div className="pt-24 bg-gray-50 min-h-screen">
      <section className="bg-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="max-w-3xl">
            <p className="text-gold-400 uppercase tracking-[0.35em] text-sm font-semibold">Community</p>
            <h1 className="mt-4 text-4xl md:text-5xl font-heading font-bold">People-powered change starts with belonging.</h1>
            <p className="mt-6 text-lg text-primary-100 leading-relaxed">
              GYS grows stronger when residents, partners, and volunteers work together. Our community programs are built to be welcoming, responsive, and measurable.
            </p>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid gap-6 md:grid-cols-3">
          {groups.map((group) => {
            const Icon = group.icon
            return (
              <div key={group.title} className="card p-8">
                <div className="w-12 h-12 rounded-2xl bg-primary-50 flex items-center justify-center text-primary-700">
                  <Icon size={24} />
                </div>
                <h2 className="mt-5 text-xl font-heading font-bold text-gray-900">{group.title}</h2>
                <p className="mt-3 text-gray-600 leading-relaxed">{group.description}</p>
              </div>
            )
          })}
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="rounded-3xl bg-white shadow-xl border border-gray-100 p-8 md:p-10">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary-700">How to get involved</p>
            <h2 className="mt-3 text-3xl font-heading font-bold text-gray-900">Become part of a trusted network for good.</h2>
            <p className="mt-4 text-gray-600 leading-relaxed">
              Attend a town hall, share your ideas, or volunteer for an upcoming outreach event. Every voice helps shape better outcomes.
            </p>
            <Link to="/contact" className="btn-primary mt-6">
              Start a Conversation <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
