import { useState, useEffect } from 'react'
import { NavLink, Link } from 'react-router-dom'
import { Menu, X, ChevronDown } from 'lucide-react'
import Logo from '../ui/Logo'

const navLinks = [
  { label: 'Home',      to: '/' },
  { label: 'About',     to: '/about' },
  { label: 'Programs',  to: '/programs' },
  { label: 'Reports',   to: '/reports' },
  { label: 'News',      to: '/news' },
  { label: 'Community', to: '/community' },
  { label: 'Contact',   to: '/contact' },
]

export default function Navbar() {
  const [open, setOpen]         = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const linkClass = ({ isActive }) =>
    `text-sm font-medium transition-colors duration-150 hover:text-gold-500 ${
      isActive ? 'text-gold-500' : 'text-white'
    }`

  const mobileLinkClass = ({ isActive }) =>
    `block px-4 py-3 text-base font-medium rounded-lg transition-colors ${
      isActive
        ? 'bg-primary-700 text-gold-400'
        : 'text-gray-800 hover:bg-primary-50 hover:text-primary-700'
    }`

  return (
    <header
      className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-gray-900 shadow-xl' : 'bg-gray-900/95 backdrop-blur-sm'
      }`}
    >
      {/* Top bar */}
      <div className="bg-primary-700 py-1.5 px-4 text-center">
        <p className="text-xs text-white font-medium tracking-wide">
          🌿 Empowering Communities · Building Futures · Transparency First
        </p>
      </div>

      {/* Main nav */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 flex-shrink-0">
            <Logo />
            <div className="hidden sm:block">
              <span className="font-heading font-bold text-white text-lg leading-tight block">
                GYS Portal
              </span>
              <span className="text-gold-400 text-xs font-medium tracking-widest uppercase">
                Transparency
              </span>
            </div>
          </Link>

          {/* Desktop links */}
          <nav className="hidden lg:flex items-center gap-6">
            {navLinks.map((link) => (
              <NavLink key={link.to} to={link.to} end={link.to === '/'} className={linkClass}>
                {link.label}
              </NavLink>
            ))}
          </nav>

          {/* CTA + hamburger */}
          <div className="flex items-center gap-3">
            <Link
              to="/donate"
              className="hidden sm:inline-flex items-center px-4 py-2 bg-gold-500 hover:bg-gold-400 text-black text-sm font-bold rounded-lg transition-colors duration-150 shadow"
            >
              Donate Now
            </Link>
            <button
              onClick={() => setOpen(!open)}
              className="lg:hidden p-2 text-white hover:text-gold-400 transition-colors"
              aria-label="Toggle menu"
            >
              {open ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="lg:hidden bg-white border-t border-gray-100 shadow-xl">
          <nav className="max-w-7xl mx-auto px-4 py-3 flex flex-col gap-1">
            {navLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === '/'}
                className={mobileLinkClass}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </NavLink>
            ))}
            <Link
              to="/donate"
              onClick={() => setOpen(false)}
              className="mt-2 btn-gold justify-center"
            >
              Donate Now
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}
