import { useNavigate, Link } from 'react-router-dom'
import { clearToken, isAuthed } from '../lib/auth'

export default function NavBar() {
  const nav = useNavigate()

  const logout = () => {
    clearToken()
    nav('/login')
  }

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
        <Link to="/patients" className="text-lg font-semibold">EHR Lab Order System</Link>
        <nav className="flex items-center gap-4 text-sm">
          <Link to="/patients" className="text-gray-700 hover:text-gray-900">Patients</Link>
          <Link to="/labs" className="text-gray-700 hover:text-gray-900">Labs</Link>
          {isAuthed() ? (
            <button onClick={logout} className="rounded border px-3 py-1 text-gray-700 hover:bg-gray-50">Logout</button>
          ) : (
            <Link to="/login" className="rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-700">Login</Link>
          )}
        </nav>
      </div>
    </header>
  )
}

