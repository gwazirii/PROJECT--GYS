import { Link } from 'react-router-dom'
import {
  ArrowRight, Shield, BarChart3, Users, Heart,
  FileText, Globe, CheckCircle, Star,
} from 'lucide-react'
import SectionHeader from '../components/ui/SectionHeader'
import StatCard from '../components/ui/StatCard'

const stats = [
  { value: '12,000+', label: 'Lives Impacted',      icon: Users,    color: 'primary' },
  { value: '47',      label: 'Active Programs',     icon: Globe,    color: 'gold' },
  { value: '98%',     label: 'Fund Transparency',   icon: Shield,   color: 'black' },
  { value: '15+',     label: 'Years of Service',    icon: Star,     color: 'primary' },
]

const programs = [
  {
    icon: '🎓',
    title: 'Education Initiative',
    desc:  'Scholarships, school supplies, and mentorship programs for underprivileged youth.',
    color: 'border-primary-500',
  },
  {
    icon: '🏥',
    title: 'Community Health',
    desc:  'Free medical clinics, health screenings, and wellness campaigns across regions.',
    color: 'border-gold-500',
  },
  {
    icon: '🌱',
    title: 'Sustainable Agriculture',
    desc:  'Training farmers in modern techniques to boost food security and income.',
    color: 'border-primary-700',
  },
  {
    icon: '💡',
    title: 'Youth Empowerment',
    desc:  'Skills training, entrepreneurship support, and job placement for young people.',
    color: 'border-gold-400',
  },
]

const values = [
  { title: 'Transparency',  desc: 'Every cedi is accounted for — we publish full financial reports.' },
  { title: 'Accountability', desc: 'We hold ourselves to the highest standards of governance.' },
  { title: 'Community',     desc: 'Decisions are made with, not for, the communities we serve.' },
  { title: 'Impact',        desc: 'Measurable outcomes drive every program we run.' },
]

const testimonials = [
  {
    name:  'Ama Boateng',
    role:  'Program Beneficiary',
    text:  'The GYS Education Initiative changed my life. I now have a full scholarship and a clear path forward.',
    img:   'https://i.pravatar.cc/80?img=47',
  },
  {
    name:  'Kwame Asante',
    role:  'Community Partner',
    text:  'Working with GYS has been a model of how NGOs should operate — transparent, efficient, and people-first.',
    img:   'https://i.pravatar.cc/80?img=12',
  },
  {
    name:  'Dr. Abena Mensah',
    role:  'Health Program Volunteer',
    text:  "The community health camps reached villages that had never seen a doctor. GYS makes the impossible happen.",
    img:   'https://i.pravatar.cc/80?img=32',
  },
]

export default function Home() {
  return (
    <>
      {/* ── HERO ── */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gray-900">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0"
            style={{
              backgroundImage: 'radial-gradient(circle at 25% 25%, #15803d 0%, transparent 50%), radial-gradient(circle at 75% 75%, #f59e0b 0%, transparent 50%)',
            }}
          />
        </div>
        {/* Grid overlay */}
        <div
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.1) 1px, transparent 1px)',
            backgroundSize: '60px 60px',
          }}
        />

        <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 text-center pt-24 pb-16">
          {/* Eyebrow badge */}
          <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-700/30 border border-primary-600 text-primary-300 text-sm font-medium mb-6">
            <Shield size={14} /> Trusted NGO Since 2009
          </span>

          <h1 className="font-heading font-extrabold text-5xl md:text-6xl lg:text-7xl text-white leading-tight">
            Transparency &amp;{' '}
            <span className="text-gold-400">Accountability</span>
            {' '}for a Better Tomorrow
          </h1>

          <p className="mt-6 text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
            GYS is dedicated to empowering communities through transparent programs,
            open financial reporting, and genuine grassroots engagement.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/programs" className="btn-primary text-base px-8 py-4">
              Explore Programs <ArrowRight size={18} />
            </Link>
            <Link to="/reports" className="btn-outline text-base px-8 py-4 border-white text-white hover:bg-white hover:text-gray-900">
              View Reports <FileText size={18} />
            </Link>
          </div>

          {/* Mini stats */}
          <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
            {stats.map((s) => (
              <div key={s.label}>
                <p className="font-heading font-extrabold text-3xl text-gold-400">{s.value}</p>
                <p className="text-gray-400 text-sm mt-1">{s.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Wave divider */}
        <div className="absolute bottom-0 inset-x-0">
          <svg viewBox="0 0 1440 80" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
            <path d="M0 80L1440 80L1440 40C1200 80 960 0 720 20C480 40 240 0 0 40L0 80Z" fill="white" />
          </svg>
        </div>
      </section>

      {/* ── STATS CARDS ── */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {stats.map((s) => (
              <StatCard key={s.label} {...s} />
            ))}
          </div>
        </div>
      </section>

      {/* ── ABOUT SNAPSHOT ── */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 lg:grid-cols-2 gap-14 items-center">
          <div>
            <SectionHeader
              eyebrow="Who We Are"
              title="Building Communities Through Transparent Action"
              subtitle="GYS (Grow Your Society) is an NGO founded on the belief that communities thrive when resources are distributed fairly and decisions are made openly."
            />
            <ul className="mt-8 space-y-3">
              {[
                '100% publicly audited financial records',
                'Community-led program design',
                'Third-party impact verification',
                'Annual transparency summit',
              ].map((item) => (
                <li key={item} className="flex items-center gap-3 text-gray-700">
                  <CheckCircle size={18} className="text-primary-600 shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
            <div className="mt-8 flex gap-4">
              <Link to="/about" className="btn-primary">
                Learn More <ArrowRight size={16} />
              </Link>
              <Link to="/reports" className="btn-outline">
                Our Reports
              </Link>
            </div>
          </div>

          {/* Visual card grid */}
          <div className="grid grid-cols-2 gap-4">
            {values.map((v) => (
              <div key={v.title} className="card p-6">
                <div className="w-10 h-1 bg-gold-500 rounded mb-3" />
                <h4 className="font-heading font-bold text-gray-900 mb-1">{v.title}</h4>
                <p className="text-sm text-gray-500 leading-relaxed">{v.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PROGRAMS ── */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Our Work"
            title="Programs Making Real Impact"
            subtitle="From education to health, every program is designed with measurable outcomes and community ownership."
            center
          />
          <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {programs.map((p) => (
              <div key={p.title} className={`card p-6 border-t-4 ${p.color}`}>
                <span className="text-4xl mb-4 block">{p.icon}</span>
                <h3 className="font-heading font-bold text-gray-900 mb-2">{p.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
          <div className="mt-10 text-center">
            <Link to="/programs" className="btn-primary">
              View All Programs <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── TRANSPARENCY BANNER ── */}
      <section className="bg-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          {[
            { icon: BarChart3, label: 'Financial Reports', desc: 'Quarterly & annual reports published publicly' },
            { icon: FileText,  label: 'Program Audits',   desc: 'Independent third-party audits every year' },
            { icon: Users,     label: 'Community Forums', desc: 'Open meetings with stakeholders every quarter' },
          ].map(({ icon: Icon, label, desc }) => (
            <div key={label} className="flex flex-col items-center gap-3">
              <div className="w-14 h-14 rounded-2xl bg-primary-600 flex items-center justify-center">
                <Icon size={28} className="text-gold-400" />
              </div>
              <h4 className="font-heading font-bold text-white text-lg">{label}</h4>
              <p className="text-primary-100 text-sm">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── TESTIMONIALS ── */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <SectionHeader
            eyebrow="Voices from the Community"
            title="Stories of Real Change"
            center
          />
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((t) => (
              <div key={t.name} className="card p-8">
                <div className="flex gap-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={14} className="text-gold-500 fill-gold-500" />
                  ))}
                </div>
                <p className="text-gray-600 italic leading-relaxed mb-6">"{t.text}"</p>
                <div className="flex items-center gap-3 border-t pt-4">
                  <img src={t.img} alt={t.name} className="w-10 h-10 rounded-full object-cover" />
                  <div>
                    <p className="font-semibold text-gray-900 text-sm">{t.name}</p>
                    <p className="text-xs text-gray-500">{t.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── DONATE CTA ── */}
      <section className="py-20 bg-gray-900 relative overflow-hidden">
        <div className="absolute inset-0 opacity-20"
          style={{ backgroundImage: 'radial-gradient(circle at 60% 50%, #15803d 0%, transparent 60%)' }}
        />
        <div className="relative z-10 max-w-3xl mx-auto px-4 text-center">
          <Heart size={48} className="text-gold-400 mx-auto mb-4" />
          <h2 className="font-heading font-extrabold text-4xl text-white mb-4">
            Join Us in Creating Change
          </h2>
          <p className="text-gray-300 text-lg mb-8">
            Every contribution, big or small, directly funds programs that uplift communities.
            Your generosity is fully traceable through our public ledger.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/donate" className="btn-gold text-base px-8 py-4">
              Donate Now <Heart size={18} />
            </Link>
            <Link to="/community" className="btn-outline border-white text-white hover:bg-white hover:text-gray-900 text-base px-8 py-4">
              Get Involved
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
