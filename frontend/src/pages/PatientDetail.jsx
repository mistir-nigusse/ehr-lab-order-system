import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../lib/api'

export default function PatientDetail() {
  const { id } = useParams()
  const pid = Number(id)
  const nav = useNavigate()
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const [encType, setEncType] = useState('OUT')
  const [encMsg, setEncMsg] = useState('')
  const [encId, setEncId] = useState(null)

  const [noteText, setNoteText] = useState('')
  const [noteMsg, setNoteMsg] = useState('')

  const [probText, setProbText] = useState('')
  const [probCode, setProbCode] = useState('')
  const [allSub, setAllSub] = useState('')
  const [allSeverity, setAllSeverity] = useState('')
  const [allReaction, setAllReaction] = useState('')
  const [medRx, setMedRx] = useState('')
  const [medDose, setMedDose] = useState('')
  const [medRoute, setMedRoute] = useState('')
  const [medStart, setMedStart] = useState('')
  const [ehrMsg, setEhrMsg] = useState('')

  const [orderTests, setOrderTests] = useState('')
  const [orderMsg, setOrderMsg] = useState('')

  async function load() {
    try {
      setLoading(true)
      const s = await api.getPatientSummary(pid)
      setSummary(s)
      setError('')
    } catch (e) {
      setError(e.message || 'Failed to load summary')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [pid])

  async function startEncounter(e) {
    e.preventDefault()
    setEncMsg('')
    try {
      const r = await api.createEncounter({ patientId: pid, type: encType })
      setEncId(r.encounterId)
      setEncMsg(`Encounter #${r.encounterId} started`)
    } catch (err) {
      setEncMsg(err.message || 'Failed to start encounter')
    }
  }

  async function appendNote(e) {
    e.preventDefault()
    setNoteMsg('')
    try {
      const eid = encId || (summary?.notes_recent?.[0]?.encounterId)
      if (!eid) throw new Error('No encounterId; start an encounter first')
      const r = await api.appendNote({ patientId: pid, encounterId: eid, text: noteText })
      setNoteMsg(`Note #${r.noteId} saved`)
      setNoteText('')
      await load()
    } catch (err) {
      setNoteMsg(err.message || 'Failed to add note')
    }
  }

  async function addProblem(e) {
    e.preventDefault()
    setEhrMsg('')
    try {
      await api.addProblem({ patientId: pid, code: probCode || undefined, text: probText || undefined, active: true })
      setProbCode(''); setProbText('')
      await load()
      setEhrMsg('Problem added')
    } catch (e) { setEhrMsg(e.message) }
  }

  async function addAllergy(e) {
    e.preventDefault()
    setEhrMsg('')
    try {
      await api.addAllergy({ patientId: pid, substance_code: allSub || undefined, severity: allSeverity || undefined, reaction: allReaction || undefined })
      setAllSub(''); setAllSeverity(''); setAllReaction('')
      await load()
      setEhrMsg('Allergy added')
    } catch (e) { setEhrMsg(e.message) }
  }

  async function addMedication(e) {
    e.preventDefault()
    setEhrMsg('')
    try {
      await api.addMedication({ patientId: pid, rx_code: medRx || undefined, dose: medDose || undefined, route: medRoute || undefined, start: medStart || undefined })
      setMedRx(''); setMedDose(''); setMedRoute(''); setMedStart('')
      await load()
      setEhrMsg('Medication added')
    } catch (e) { setEhrMsg(e.message) }
  }

  async function placeOrder(e) {
    e.preventDefault()
    setOrderMsg('')
    try {
      const eid = encId || (summary?.notes_recent?.[0]?.encounterId)
      if (!eid) throw new Error('No encounterId; start an encounter first')
      const tests = orderTests.split(',').map(t=>t.trim()).filter(Boolean)
      const r = await api.placeOrder({ encounterId: eid, tests })
      setOrderMsg(`Order #${r.orderId} placed`)
      setOrderTests('')
    } catch (e) { setOrderMsg(e.message) }
  }

  if (loading) return <div className="p-6">Loading...</div>
  if (error) return <div className="p-6 text-red-600">{error}</div>
  if (!summary) return null

  return (
    <div className="mx-auto max-w-6xl p-6">
      <button className="mb-4 text-sm text-gray-600" onClick={()=>nav(-1)}>&larr; Back</button>
      <h1 className="text-xl font-semibold">{summary.patient.name} <span className="text-sm font-normal text-gray-600">(MRN: {summary.patient.mrn})</span></h1>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="rounded border bg-white p-4 shadow-sm">
          <h2 className="font-medium">Encounter & Notes</h2>
          <form onSubmit={startEncounter} className="mt-3 flex items-end gap-2">
            <div>
              <label className="block text-sm text-gray-700">Type</label>
              <select className="mt-1 rounded border p-2" value={encType} onChange={(e)=>setEncType(e.target.value)}>
                <option>OUT</option>
                <option>ER</option>
                <option>IN</option>
              </select>
            </div>
            <button className="rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700">Start Encounter</button>
          </form>
          {encMsg && <p className="mt-2 text-sm text-gray-600">{encMsg}</p>}

          <form onSubmit={appendNote} className="mt-4">
            <label className="block text-sm text-gray-700">Note Text</label>
            <textarea className="mt-1 w-full rounded border p-2" rows={3} value={noteText} onChange={(e)=>setNoteText(e.target.value)} required />
            <div className="mt-2 flex items-center gap-2">
              <button className="rounded border px-3 py-1 hover:bg-gray-50">Append Note</button>
              {noteMsg && <span className="text-sm text-gray-600">{noteMsg}</span>}
            </div>
          </form>

          <div className="mt-4">
            <h3 className="text-sm font-medium">Recent Notes</h3>
            <ul className="mt-2 space-y-2">
              {summary.notes_recent.map(n=> (
                <li key={n.id} className="rounded border p-2">
                  <div className="text-sm text-gray-600">#{n.id} • {n.author} • {n.created_at}</div>
                  <div>{n.text}</div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="rounded border bg-white p-4 shadow-sm">
          <h2 className="font-medium">Clinical Data</h2>
          {ehrMsg && <p className="mt-1 text-sm text-gray-600">{ehrMsg}</p>}
          <form onSubmit={addProblem} className="mt-3 grid grid-cols-3 gap-2">
            <input placeholder="Problem text" className="col-span-2 rounded border p-2" value={probText} onChange={(e)=>setProbText(e.target.value)} />
            <input placeholder="Code" className="rounded border p-2" value={probCode} onChange={(e)=>setProbCode(e.target.value)} />
            <button className="col-span-3 rounded border px-3 py-1 hover:bg-gray-50">Add Problem</button>
          </form>
          <form onSubmit={addAllergy} className="mt-3 grid grid-cols-3 gap-2">
            <input placeholder="Substance" className="rounded border p-2" value={allSub} onChange={(e)=>setAllSub(e.target.value)} />
            <input placeholder="Severity" className="rounded border p-2" value={allSeverity} onChange={(e)=>setAllSeverity(e.target.value)} />
            <input placeholder="Reaction" className="rounded border p-2" value={allReaction} onChange={(e)=>setAllReaction(e.target.value)} />
            <button className="col-span-3 rounded border px-3 py-1 hover:bg-gray-50">Add Allergy</button>
          </form>
          <form onSubmit={addMedication} className="mt-3 grid grid-cols-4 gap-2">
            <input placeholder="Rx Code" className="rounded border p-2" value={medRx} onChange={(e)=>setMedRx(e.target.value)} />
            <input placeholder="Dose" className="rounded border p-2" value={medDose} onChange={(e)=>setMedDose(e.target.value)} />
            <input placeholder="Route" className="rounded border p-2" value={medRoute} onChange={(e)=>setMedRoute(e.target.value)} />
            <input type="date" className="rounded border p-2" value={medStart} onChange={(e)=>setMedStart(e.target.value)} />
            <button className="col-span-4 rounded border px-3 py-1 hover:bg-gray-50">Add Medication</button>
          </form>

          <div className="mt-4">
            <h3 className="text-sm font-medium">Problems</h3>
            <ul className="mt-2 space-y-2">
              {summary.problems.map(pr => (
                <li key={pr.id} className="rounded border p-2 text-sm">
                  <div className="text-gray-700">{pr.text} {pr.code ? `(${pr.code})` : ''}</div>
                  <div className="text-gray-500">Active: {String(pr.active)} • {pr.created_at}</div>
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h3 className="text-sm font-medium">Allergies</h3>
            <ul className="mt-2 space-y-2 text-sm">
              {summary.allergies.map(a => (
                <li key={a.id} className="rounded border p-2">
                  <div>{a.substance_code} • {a.severity}</div>
                  <div className="text-gray-500">{a.reaction} • {a.recorded_at}</div>
                </li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <h3 className="text-sm font-medium">Medications</h3>
            <ul className="mt-2 space-y-2 text-sm">
              {summary.medications.map(m => (
                <li key={m.id} className="rounded border p-2">
                  <div>{m.rx_code} • {m.dose} • {m.route}</div>
                  <div className="text-gray-500">Start: {m.start} {m.end ? `• End: ${m.end}` : ''}</div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="rounded border bg-white p-4 shadow-sm">
          <h2 className="font-medium">Orders</h2>
          <form onSubmit={placeOrder} className="mt-3">
            <label className="block text-sm text-gray-700">Tests (comma separated)</label>
            <input className="mt-1 w-full rounded border p-2" placeholder="CBC, BMP" value={orderTests} onChange={(e)=>setOrderTests(e.target.value)} />
            <div className="mt-2 flex items-center gap-2">
              <button className="rounded border px-3 py-1 hover:bg-gray-50">Place Order</button>
              {orderMsg && <span className="text-sm text-gray-600">{orderMsg}</span>}
            </div>
          </form>

          <div className="mt-4">
            <h3 className="text-sm font-medium">Recent Lab Results</h3>
            <ul className="mt-2 space-y-2 text-sm">
              {summary.lab_results_recent.map(r => (
                <li key={r.id} className="rounded border p-2">
                  <div>{r.test_code} = {r.value} {r.units || ''}</div>
                  <div className="text-gray-500">Resulted: {r.resulted_at || r.received_at}</div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
