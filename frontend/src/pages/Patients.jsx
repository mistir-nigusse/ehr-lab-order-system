import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../lib/api'

export default function Patients() {
  const [mrn, setMrn] = useState('')
  const [name, setName] = useState('')
  const [dob, setDob] = useState('')
  const [gender, setGender] = useState('')
  const [formMsg, setFormMsg] = useState('')

  const [q, setQ] = useState('')
  const [results, setResults] = useState([])
  const [searchMsg, setSearchMsg] = useState('')

  useEffect(() => {
    if (!q) { setResults([]); return }
    const t = setTimeout(async () => {
      try {
        setSearchMsg('')
        const r = await api.searchPatients(q)
        setResults(r)
      } catch (e) {
        setSearchMsg(e.message || 'Search failed')
      }
    }, 300)
    return () => clearTimeout(t)
  }, [q])

  async function create(e) {
    e.preventDefault()
    setFormMsg('')
    try {
      const p = await api.createPatient({ mrn, name, dob: dob || undefined, gender: gender || undefined })
      setFormMsg(`Created patient #${p.patientId}`)
      setMrn(''); setName(''); setDob(''); setGender('')
    } catch (e) {
      setFormMsg(e.message || 'Create failed')
    }
  }

  return (
    <div className="mx-auto max-w-6xl p-6">
      <h1 className="text-xl font-semibold">Patients</h1>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <form onSubmit={create} className="rounded border bg-white p-4 shadow-sm">
          <h2 className="font-medium">Create Patient</h2>
          {formMsg && <p className="mt-2 text-sm text-gray-600">{formMsg}</p>}
          <div className="mt-4 grid gap-3">
            <div>
              <label className="block text-sm text-gray-700">MRN</label>
              <input value={mrn} onChange={(e)=>setMrn(e.target.value)} required className="mt-1 w-full rounded border p-2" />
            </div>
            <div>
              <label className="block text-sm text-gray-700">Name</label>
              <input value={name} onChange={(e)=>setName(e.target.value)} required className="mt-1 w-full rounded border p-2" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm text-gray-700">DOB</label>
                <input type="date" value={dob} onChange={(e)=>setDob(e.target.value)} className="mt-1 w-full rounded border p-2" />
              </div>
              <div>
                <label className="block text-sm text-gray-700">Gender</label>
                <input value={gender} onChange={(e)=>setGender(e.target.value)} className="mt-1 w-full rounded border p-2" />
              </div>
            </div>
            <button className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">Create</button>
          </div>
        </form>

        <div className="rounded border bg-white p-4 shadow-sm">
          <h2 className="font-medium">Search</h2>
          <input value={q} onChange={(e)=>setQ(e.target.value)} placeholder="Name or MRN" className="mt-3 w-full rounded border p-2" />
          {searchMsg && <p className="mt-2 text-sm text-red-600">{searchMsg}</p>}
          <ul className="mt-4 divide-y">
            {results.map(r => (
              <li key={r.id} className="py-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">{r.name}</div>
                    <div className="text-sm text-gray-600">MRN: {r.mrn}</div>
                  </div>
                  <Link to={`/patients/${r.id}`} className="rounded border px-3 py-1 text-sm hover:bg-gray-50">View</Link>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
