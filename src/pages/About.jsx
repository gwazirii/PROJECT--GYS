import { Link } from 'react-router-dom'
import { ArrowRight, Target, Eye, Heart, Award } from 'lucide-react'
import PageHero from '../components/ui/PageHero'
import SectionHeader from '../components/ui/SectionHeader'

const team = [
  { name: 'Emmanuel Gyasi',  role: 'Executive Director',     img: 'https://i.pravatar.cc/160?img=11' },
  { name: 'Akosua Darko',    role: 'Programs Director',      img: 'https://i.pravatar.cc/160?img=45' },
  { name: 'Kofi Mensah',     role: 'Finance Manager',        img: 'https://i.pravatar.cc/160?img=15' },
  { name: 'Abena Osei',      role: 'Community Engagement',   img: 'https://i.pravatar.cc/160?img=49' },
  { name: 'Yaw Boateng',     role: 'M&E Officer',           img: 'https://i.pravatar.cc/160?img=22' },
  { name: 'Gifty Antwi',     role: 'Communications Lead',   img: 'https://i.pravatar.cc/160?img=38' },
]

const milestones = [
  { year: '2009', event: 'GYS founded with a mission to empower marginalised communities.' },
  { year: '2012', event: 'Launched first scholarship program — 120 beneficiaries in year one.' },
  { year: '2015', event: 'Expanded to 5 regions; received first international funding.' },
  { year: '2018', event: 'Introduced open financial ledger — first NGO in the region to do so.' },
  { year: '2021', event: 'Crossed 10,000 lives impacted milestone.' },
  { year: '2024', event: 'Launched GYS Transparency Portal for real-time accountability.' },
]

export default function About() {
  return (
    <>
      <PageHero
        title="About GYS"
        subtitle="We are a non-profit organisation committed to community empowerment, transparency, and lasting social impact."
      />

      {/* Mission / Vision / Values */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: Target,
              color: 'bg-primary-50 text-primary-700',
              title: 'Our Mission',
              text: 'To uplift marginalised communities through transparent, community-led programs that create measurable, lasting change.',
            },
            {
              icon: Eye,
              color: 'bg-gold-50 text-gold-700',
              title: 'Our Vision',
              text: 'A world where every community has the resources, knowledge, and opportunity to thrive without barriers.',
            },
            {
              icon: Heart,
              color: 'bg-gray-100 text-gray-800',
              title: 'Our Values',
              text: 'Transparency, accountability, community ownership, inclusivity, and evidence-based impact measurement.',
            },
          ].map(({ icon: Icon, color, title, text }) => (
            <div key={title} className="card p-8 text-center">
              <span className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 ${color}`}>
                <Icon size={32} />
              </span>
              <h3 className="font-heading font-bold text-xl mb-3">{title}</h3>
              <p className="text-gray-500 leading-relaxed">{text}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Story */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">
          <div>
            <SectionHeader
              eyebrow="Our Story"
              title="From a Small Office to National Impact"
              subtitle="What started as a grassroots initiative in Accra has grown into a nationally recognised organisation touching lives in 8 regions."
            />
            <div className="mt-8 space-y-4 text-gray-600 leading-relaxed">
              <p>
                GYS was founded in 2009 by a group of young professionals who believed that the biggest
                barrier to community development was not the lack of resources — it was the lack of
                transparency in how those resources were used.
              </p>
              <p>
                We built our organisation on a radical promise: every donor, every community member,
                and every partner would have full access to our financials, program performance data,
                and governance records.
              </p>
              <p>
                Today, GYS operates across 8 regions, runs 47 active programs, and has directly
                impacted over 12,000 lives. Our transparency portal is the culmination of 15 years
                of building trust, one report at a time.
              </p>
            </div>
          </div>

          {/* Timeline */}
          <div className="space-y-4">
            {milestones.map((m, i) => (
              <div key={m.year} className="flex gap-4 items-start">
                <div className="flex flex-col items-center">
                  <div className="w-10 h-10 rounded-full bg-primary-700 text-white flex items-center justify-center font-bold text-xs shrink-0">
                    {m.year.slice(2)}
                  </div>
                  {i < milestones.length - 1 && <div className="w-0.5 h-8 bg-primary-200 mt-1" />}
                </div>
                <div className="pb-4">
                  <span className="text-gold-600 font-bold text-sm">{m.year}</span>
                  <p className="text-gray-600 text-sm mt-0.5">{m.event}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="The People"
            title="Meet Our Leadership Team"
            subtitle="Passionate professionals dedicated to transparent community development."
            center
          />
          <div className="mt-12 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6">
            {team.map((m) => (
              <div key={m.name} className="text-center group">
                <div className="relative mx-auto w-24 h-24 mb-3 rounded-full overflow-hidden ring-4 ring-transparent group-hover:ring-primary-400 transition-all duration-300">
                  <img src={m.img} alt={m.name} className="w-full h-full object-cover" />
                </div>
                <p className="font-semibold text-gray-900 text-sm">{m.name}</p>
                <p className="text-xs text-primary-600 mt-0.5">{m.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Partners */}
      <section className="py-16 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gold-400 font-semibold uppercase text-sm tracking-widest mb-8">
            Trusted by Partners &amp; Donors Worldwide
          </p>
          <div className="flex flex-wrap justify-center gap-8 opacity-60">
            {['UNDP', 'World Bank', 'USAID', 'GIZ', 'Oxfam', 'UNICEF'].map((p) => (
              <span key={p} className="text-white font-heading font-bold text-lg">{p}</span>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-primary-700">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <Award size={40} className="text-gold-400 mx-auto mb-4" />
          <h2 className="font-heading font-bold text-3xl text-white mb-3">
            Partner with GYS
          </h2>
          <p className="text-primary-100 mb-7">
            Whether you are an individual donor, a foundation, or a government agency,
            we welcome partnerships built on shared values of transparency and impact.
          </p>
          <Link to="/contact" className="btn-gold">
            Get in Touch <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </>
  )
}
