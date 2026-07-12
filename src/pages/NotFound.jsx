import { Home, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-24">
      <div className="max-w-xl text-center card p-10 md:p-14">
        <p className="text-sm font-semibold uppercase tracking-[0.35em] text-primary-700">404</p>
        <h1 className="mt-4 text-4xl md:text-5xl font-heading font-bold text-gray-900">Page not found</h1>
        <p className="mt-4 text-lg text-gray-600 leading-relaxed">
          The page you are looking for might have moved or no longer exists. Let’s return you to the main experience.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link to="/" className="btn-primary">
            <Home size={16} /> Go Home
          </Link>
          <button onClick={() => window.history.back()} className="btn-outline">
            <ArrowLeft size={16} /> Go Back
          </button>
        </div>
      </div>
    </div>
  )
}
