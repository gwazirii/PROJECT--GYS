import { Heart, ShieldCheck, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'

const waysToGive = [
  { title: 'One-Time Gift', amount: 'GH₵ 100+', description: 'Fund immediate community support and education needs.' },
  { title: 'Monthly Support', amount: 'GH₵ 50+', description: 'Create lasting impact with recurring resources for our programs.' },
  { title: 'Corporate Partnership', amount: 'Custom', description: 'Sponsor outreach, health campaigns, or youth entrepreneurship.' },
]

export default function Donate() {
  return (
    <div className="pt-24 bg-gray-50 min-h-screen">
      <section className="bg-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="max-w-3xl">
            <p className="text-gold-400 uppercase tracking-[0.35em] text-sm font-semibold">Donate</p>
            <h1 className="mt-4 text-4xl md:text-5xl font-heading font-bold">Help us turn resources into real impact.</h1>
            <p className="mt-6 text-lg text-primary-100 leading-relaxed">
              Your generosity helps fund school support, health outreach, and community development projects that reach those who need them most.
            </p>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="card p-8 md:p-10">
          <div className="inline-flex items-center rounded-full bg-gold-100 px-3 py-1 text-sm font-semibold text-gold-700">
            <Heart size={16} className="mr-2" /> Secure giving
          </div>
          <h2 className="mt-4 text-3xl font-heading font-bold text-gray-900">Every contribution is tracked and reported.</h2>
          <p className="mt-4 text-gray-600 leading-relaxed">
            We publish transparent progress updates so donors can see how support is used in the field.
          </p>
          <div className="mt-6 space-y-3">
            {[
              'Verified program delivery with quarterly updates',
              'Independent oversight for major initiatives',
              'Flexible options for individuals and institutions',
            ].map((point) => (
              <div key={point} className="flex items-center gap-3 text-gray-700">
                <ShieldCheck size={18} className="text-primary-700" />
                <span>{point}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          {waysToGive.map((item) => (
            <div key={item.title} className="card p-6">
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary-700">{item.amount}</p>
              <h3 className="mt-2 text-xl font-heading font-bold text-gray-900">{item.title}</h3>
              <p className="mt-2 text-gray-600 leading-relaxed">{item.description}</p>
            </div>
          ))}
          <Link to="/contact" className="btn-primary mt-2">
            Partner With Us <ArrowRight size={16} />
          </Link>
        </div>
      </section>
    </div>
  )
}
