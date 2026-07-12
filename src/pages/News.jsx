import { useState } from 'react'
import { Calendar, Clock, ArrowRight, Tag } from 'lucide-react'
import PageHero from '../components/ui/PageHero'
import SectionHeader from '../components/ui/SectionHeader'

const categories = ['All', 'Programs', 'Community', 'Events', 'Reports', 'Partnerships']

const articles = [
  {
    id: 1,
    category: 'Programs',
    date: 'December 10, 2024',
    readTime: '4 min read',
    title: 'GYS Scholarship Fund Reaches 3,200 Beneficiaries in 2024',
    excerpt: 'Our flagship scholarship program has surpassed its annual target, providing over 3,200 students with full and partial scholarships for the 2024/2025 academic year.',
    img: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=600&q=80',
    featured: true,
  },
  {
    id: 2,
    category: 'Community',
    date: 'November 28, 2024',
    readTime: '3 min read',
    title: 'Community Health Camp Reaches 2,000 in Northern Region',
    excerpt: 'Our mobile health unit conducted a three-day health screening camp in the Northern Region, reaching communities that had never had access to professional healthcare.',
    img: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=600&q=80',
    featured: false,
  },
  {
    id: 3,
    category: 'Reports',
    date: 'November 15, 2024',
    readTime: '5 min read',
    title: 'Q3 2024 Impact Report: Highlights and Key Findings',
    excerpt: 'We have published our third-quarter impact report for 2024. The data shows significant improvements across all program areas, with particularly strong results in our agriculture initiative.',
    img: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&q=80',
    featured: false,
  },
  {
    id: 4,
    category: 'Events',
    date: 'October 30, 2024',
    readTime: '2 min read',
    title: 'Annual Transparency Summit 2024 — Register Now',
    excerpt: 'Join us for our annual Transparency Summit where we present our full year financial performance, program outcomes, and answer questions from the public and our donors.',
    img: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600&q=80',
    featured: false,
  },
  {
    id: 5,
    category: 'Partnerships',
    date: 'October 12, 2024',
    readTime: '3 min read',
    title: 'GYS Signs MoU with Ministry of Education for School Library Project',
    excerpt: 'We are proud to announce a formal partnership with the Ministry of Education to expand our school library project to an additional 15 schools in rural areas.',
    img: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600&q=80',
    featured: false,
  },
  {
    id: 6,
    category: 'Programs',
    date: 'September 20, 2024',
    readTime: '4 min read',
    title: "Women's Empowerment Program Graduates 200 Entrepreneurs",
    excerpt: "Our women's empowerment cohort for 2024 celebrated its graduation ceremony. The 200 graduates have collectively started 156 businesses and created over 400 jobs.",
    img: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600&q=80',
    featured: false,
  },
]

export default function News() {
  const [active, setActive] = useState('All')

  const filtered = active === 'All'
    ? articles
    : articles.filter((a) => a.category === active)

  const featured = filtered.find((a) => a.featured) || filtered[0]
  const rest = filtered.filter((a) => a.id !== featured?.id)

  return (
    <>
      <PageHero
        title="News & Updates"
        subtitle="Stay informed about our programs, community stories, events, and impact reports."
      />

      {/* Filters */}
      <section className="py-6 bg-white border-b sticky top-[calc(4rem+1.75rem)] z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap gap-2">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setActive(c)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-colors ${
                active === c ? 'bg-primary-700 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Featured */}
          {featured && (
            <div className="card mb-10 grid grid-cols-1 lg:grid-cols-5 overflow-hidden">
              <div className="lg:col-span-3 relative h-64 lg:h-auto">
                <img src={featured.img} alt={featured.title} className="w-full h-full object-cover" />
                <span className="absolute top-4 left-4 badge bg-gold-500 text-black font-semibold text-xs">
                  Featured
                </span>
              </div>
              <div className="lg:col-span-2 p-8 flex flex-col justify-center">
                <span className="badge bg-primary-100 text-primary-700 text-xs mb-3 w-fit">
                  {featured.category}
                </span>
                <h2 className="font-heading font-bold text-2xl text-gray-900 mb-3 leading-snug">
                  {featured.title}
                </h2>
                <p className="text-gray-500 text-sm leading-relaxed mb-5">{featured.excerpt}</p>
                <div className="flex items-center gap-4 text-xs text-gray-400 mb-6">
                  <span className="flex items-center gap-1"><Calendar size={12} />{featured.date}</span>
                  <span className="flex items-center gap-1"><Clock size={12} />{featured.readTime}</span>
                </div>
                <button className="btn-primary w-fit">
                  Read More <ArrowRight size={15} />
                </button>
              </div>
            </div>
          )}

          {/* Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {rest.map((a) => (
              <article key={a.id} className="card flex flex-col group">
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={a.img}
                    alt={a.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <span className="absolute top-3 left-3 badge bg-white/90 text-primary-700 text-xs font-medium">
                    <Tag size={10} className="mr-1" />{a.category}
                  </span>
                </div>
                <div className="p-6 flex flex-col flex-1">
                  <div className="flex items-center gap-3 text-xs text-gray-400 mb-3">
                    <span className="flex items-center gap-1"><Calendar size={11} />{a.date}</span>
                    <span className="flex items-center gap-1"><Clock size={11} />{a.readTime}</span>
                  </div>
                  <h3 className="font-heading font-bold text-gray-900 mb-2 leading-snug group-hover:text-primary-700 transition-colors">
                    {a.title}
                  </h3>
                  <p className="text-gray-500 text-sm leading-relaxed flex-1 mb-4">{a.excerpt}</p>
                  <button className="text-primary-700 font-semibold text-sm flex items-center gap-1 hover:gap-2 transition-all w-fit">
                    Read More <ArrowRight size={14} />
                  </button>
                </div>
              </article>
            ))}
          </div>

          {filtered.length === 0 && (
            <p className="text-center text-gray-400 py-16">No articles in this category yet.</p>
          )}
        </div>
      </section>

      {/* Newsletter */}
      <section className="py-16 bg-primary-700">
        <div className="max-w-2xl mx-auto px-4 text-center">
          <h2 className="font-heading font-bold text-3xl text-white mb-3">Never Miss an Update</h2>
          <p className="text-primary-100 mb-7">
            Subscribe to our newsletter for program updates, impact stories, and transparency reports.
          </p>
          <form className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto" onSubmit={(e) => e.preventDefault()}>
            <input
              type="email"
              placeholder="Your email address"
              className="flex-1 px-4 py-3 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gold-400"
            />
            <button type="submit" className="btn-gold shrink-0">
              Subscribe
            </button>
          </form>
        </div>
      </section>
    </>
  )
}
