import { useNavigate, Link } from 'react-router-dom'
import { clearToken, isAuthed, getUser, getRoles } from '../lib/auth'

export default function NavBar() {
  const nav = useNavigate()

  const logout = () => {
    clearToken()
    nav('/login')
  }

  const user = getUser()
  const roleLabel = (user?.roles && user.roles.length) ? user.roles.join(', ') : null
  const roles = getRoles()

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between p-4">
        <Link to="/patients" className="text-lg font-semibold">EHR Lab Order System</Link>
        <nav className="flex items-center gap-4 text-sm">
          {(roles.includes('Physician') || roles.includes('Nurse')) && (
            <Link to="/patients" className="text-gray-700 hover:text-gray-900">Patients</Link>
          )}
          <Link to="/labs" className="text-gray-700 hover:text-gray-900">Labs</Link>
          {isAuthed() ? (
            <div className="flex items-center gap-3">
              {user && (
                <span className="text-gray-600">{user.username}{roleLabel ? ` • ${roleLabel}` : ''}</span>
              )}
              <button onClick={logout} className="rounded border px-3 py-1 text-gray-700 hover:bg-gray-50">Logout</button>
            </div>
          ) : (
            <Link to="/login" className="rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-700">Login</Link>
          )}
        </nav>
      </div>
    </header>
  )
}
