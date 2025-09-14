import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { setToken } from '../lib/auth'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('Physician')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const nav = useNavigate()

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await api.login(username, password, role)
      setToken(res.access_token)
      nav('/patients')
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-md p-6">
      <h1 className="text-xl font-semibold">Sign in</h1>
      <form onSubmit={onSubmit} className="mt-4 space-y-3">
        {error && <div className="rounded border border-red-300 bg-red-50 p-2 text-red-700 text-sm">{error}</div>}
        <div>
          <label className="block text-sm text-gray-700">Username</label>
          <input className="mt-1 w-full rounded border p-2" value={username} onChange={(e)=>setUsername(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm text-gray-700">Password</label>
          <input type="password" className="mt-1 w-full rounded border p-2" value={password} onChange={(e)=>setPassword(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm text-gray-700">Role</label>
          <select className="mt-1 w-full rounded border p-2" value={role} onChange={(e)=>setRole(e.target.value)}>
            <option>Physician</option>
            <option>Nurse</option>
            <option>LabTech</option>
          </select>
        </div>
        <button disabled={loading} className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50">{loading? 'Signing in...' : 'Sign in'}</button>
      </form>
    </div>
  )
}

