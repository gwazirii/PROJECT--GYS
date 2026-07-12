import { Link } from 'react-router-dom'
import { Mail, Phone, MapPin, Facebook, Twitter, Instagram, Youtube, ArrowRight } from 'lucide-react'
import Logo from '../ui/Logo'

const quickLinks = [
  { label: 'About Us',     to: '/about' },
  { label: 'Our Programs', to: '/programs' },
  { label: 'Reports',      to: '/reports' },
  { label: 'News & Updates', to: '/news' },
  { label: 'Community',    to: '/community' },
  { label: 'Contact',      to: '/contact' },
]

const socialLinks = [
  { icon: Facebook,  href: '#', label: 'Facebook' },
  { icon: Twitter,   href: '#', label: 'Twitter' },
  { icon: Instagram, href: '#', label: 'Instagram' },
  { icon: Youtube,   href: '#', label: 'YouTube' },
]

export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="bg-gray-900 text-gray-300">
      {/* CTA Strip */}
      <div className="bg-primary-700 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-white font-heading font-bold text-2xl">Ready to Make a Difference?</h3>
            <p className="text-primary-100 mt-1">Your support powers real change in communities.</p>
          </div>
          <Link to="/donate" className="btn-gold shrink-0">
            Donate Today <ArrowRight size={16} />
          </Link>
        </div>
      </div>

      {/* Main footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
        {/* Brand */}
        <div className="col-span-1">
          <Link to="/" className="flex items-center gap-3 mb-4">
            <Logo />
            <div>
              <span className="font-heading font-bold text-white text-lg block">GYS Portal</span>
              <span className="text-gold-400 text-xs tracking-widest uppercase">Transparency</span>
            </div>
          </Link>
          <p className="text-sm text-gray-400 leading-relaxed mb-5">
            Committed to accountability, community empowerment, and transparent governance
            for lasting social impact.
          </p>
          <div className="flex gap-3">
            {socialLinks.map(({ icon: Icon, href, label }) => (
              <a
                key={label}
                href={href}
                aria-label={label}
                className="w-9 h-9 rounded-full bg-gray-800 hover:bg-primary-700 flex items-center justify-center transition-colors"
              >
                <Icon size={16} />
              </a>
            ))}
          </div>
        </div>

        {/* Quick Links */}
        <div>
          <h4 className="font-heading font-semibold text-white mb-4">Quick Links</h4>
          <ul className="space-y-2">
            {quickLinks.map((link) => (
              <li key={link.to}>
                <Link
                  to={link.to}
                  className="text-sm text-gray-400 hover:text-gold-400 transition-colors flex items-center gap-1.5"
                >
                  <ArrowRight size={13} className="text-primary-500" />
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* Contact */}
        <div>
          <h4 className="font-heading font-semibold text-white mb-4">Contact Us</h4>
          <ul className="space-y-3 text-sm text-gray-400">
            <li className="flex items-start gap-3">
              <MapPin size={16} className="text-primary-400 mt-0.5 shrink-0" />
              <span>123 Community Drive, Accra, Ghana</span>
            </li>
            <li className="flex items-center gap-3">
              <Phone size={16} className="text-primary-400 shrink-0" />
              <a href="tel:+233000000000" className="hover:text-gold-400 transition-colors">
                +233 000 000 000
              </a>
            </li>
            <li className="flex items-center gap-3">
              <Mail size={16} className="text-primary-400 shrink-0" />
              <a href="mailto:info@gys.org" className="hover:text-gold-400 transition-colors">
                info@gys.org
              </a>
            </li>
          </ul>
        </div>

        {/* Newsletter */}
        <div>
          <h4 className="font-heading font-semibold text-white mb-4">Stay Updated</h4>
          <p className="text-sm text-gray-400 mb-4">
            Subscribe to our newsletter for updates on programs and impact reports.
          </p>
          <form className="flex flex-col gap-2" onSubmit={(e) => e.preventDefault()}>
            <input
              type="email"
              placeholder="Your email address"
              className="px-4 py-2.5 rounded-lg bg-gray-800 border border-gray-700 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <button type="submit" className="btn-primary justify-center py-2.5 text-sm">
              Subscribe
            </button>
          </form>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-800 py-5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-500">
          <p>© {year} GYS Transparency Portal. All rights reserved.</p>
          <div className="flex gap-4">
            <a href="#" className="hover:text-gray-300 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Terms of Use</a>
            <a href="#" className="hover:text-gray-300 transition-colors">Sitemap</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
