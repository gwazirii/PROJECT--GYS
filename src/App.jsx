import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import About from './pages/About'
import Programs from './pages/Programs'
import Reports from './pages/Reports'
import News from './pages/News'
import Community from './pages/Community'
import Contact from './pages/Contact'
import Donate from './pages/Donate'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index        element={<Home />}      />
          <Route path="about"     element={<About />}     />
          <Route path="programs"  element={<Programs />}  />
          <Route path="reports"   element={<Reports />}   />
          <Route path="news"      element={<News />}      />
          <Route path="community" element={<Community />} />
          <Route path="contact"   element={<Contact />}   />
          <Route path="donate"    element={<Donate />}    />
          <Route path="*"         element={<NotFound />}  />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
