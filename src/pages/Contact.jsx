import { Mail, Phone, MapPin, Send } from 'lucide-react'

const contactPoints = [
  { icon: Mail, title: 'Email', value: 'hello@gys.org', detail: 'We respond within 24 hours.' },
  { icon: Phone, title: 'Phone', value: '+233 24 000 0000', detail: 'Call us for urgent support or partnership requests.' },
  { icon: MapPin, title: 'Visit', value: 'Accra, Ghana', detail: 'Open Monday to Friday, 8am to 5pm.' },
]

export default function Contact() {
  return (
    <div className="pt-24 bg-gray-50 min-h-screen">
      <section className="bg-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="max-w-3xl">
            <p className="text-gold-400 uppercase tracking-[0.35em] text-sm font-semibold">Contact</p>
            <h1 className="mt-4 text-4xl md:text-5xl font-heading font-bold">Let’s build something meaningful together.</h1>
            <p className="mt-6 text-lg text-primary-100 leading-relaxed">
              Reach out for partnerships, volunteer opportunities, donation support, or public inquiries.
            </p>
          </div>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="card p-8 md:p-10">
          <h2 className="text-2xl font-heading font-bold text-gray-900">Send us a message</h2>
          <p className="mt-3 text-gray-600 leading-relaxed">Share a few details about your inquiry and we will follow up promptly.</p>
          <form className="mt-8 space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <input className="w-full rounded-lg border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="Your name" />
              <input className="w-full rounded-lg border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="Email address" />
            </div>
            <input className="w-full rounded-lg border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="Subject" />
            <textarea rows="5" className="w-full rounded-lg border border-gray-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="How can we help?" />
            <button className="btn-primary">
              Send Message <Send size={16} />
            </button>
          </form>
        </div>

        <div className="space-y-4">
          {contactPoints.map((item) => {
            const Icon = item.icon
            return (
              <div key={item.title} className="card p-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary-50 flex items-center justify-center text-primary-700">
                    <Icon size={20} />
                  </div>
                  <div>
                    <h3 className="font-heading font-bold text-gray-900">{item.title}</h3>
                    <p className="mt-1 font-semibold text-gray-800">{item.value}</p>
                    <p className="mt-1 text-sm text-gray-500">{item.detail}</p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </section>
    </div>
  )
}
