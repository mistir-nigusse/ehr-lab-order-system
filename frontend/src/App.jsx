import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

function App() {
  const [backendStatus, setBackendStatus] = useState('checking...')
  const [patients, setPatients] = useState([])

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((r) => r.json())
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('unreachable'))
  }, [])

  const createDemoPatient = async () => {
    const res = await fetch(`${API_BASE}/api/patients`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mrn: `MRN-${Date.now()}`, name: 'Jane Doe' }),
    })
    const json = await res.json()
    alert(`Created patientId=${json.patientId}`)
  }

  const searchPatients = async () => {
    const res = await fetch(`${API_BASE}/api/patients/search?q=Jane`)
    const json = await res.json()
    setPatients(json)
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="mx-auto max-w-4xl p-6">
        <h1 className="text-2xl font-semibold">EHR Lab Order System</h1>
        <p className="mt-2 text-sm text-gray-600">Backend: {backendStatus}</p>

        <div className="mt-6 flex gap-3">
          <button onClick={createDemoPatient} className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Create Demo Patient
          </button>
          <button onClick={searchPatients} className="rounded border border-gray-300 px-4 py-2 hover:bg-gray-100">
            Search Patients
          </button>
        </div>

        <ul className="mt-6 space-y-2">
          {patients.map((p) => (
            <li key={p.id} className="rounded border bg-white p-3">
              <div className="font-medium">{p.name}</div>
              <div className="text-sm text-gray-600">MRN: {p.mrn}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default App
