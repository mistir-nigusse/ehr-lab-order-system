import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../lib/api'
import { getRoles } from '../lib/auth'

const statuses = ['ordered','collected','in_progress','resulted','corrected']

export default function OrderDetail() {
  const { id } = useParams()
  const oid = Number(id)
  const [order, setOrder] = useState(null)
  const [results, setResults] = useState([])
  const [status, setStatus] = useState('')
  const [msg, setMsg] = useState('')
  const roles = getRoles()

  const allowedNext = useMemo(() => {
    if (!order) return []
    const current = (order.status || 'ordered')
    const map = {
      Nurse: { ordered: 'collected' },
      LabTech: { ordered: 'collected', collected: 'in_progress', in_progress: 'resulted', resulted: 'corrected' },
      Physician: { ordered: 'collected', resulted: 'corrected' },
    }
    const nextSet = new Set()
    roles.forEach(r => { const nxt = map[r]?.[current]; if (nxt) nextSet.add(nxt) })
    return Array.from(nextSet)
  }, [order, roles])

  async function load() {
    const d = await api.getOrder(oid)
    setOrder(d.order)
    setResults(d.results)
    setStatus(d.order.status)
  }
  useEffect(()=>{ load() }, [oid])

  async function updateStatus(e){
    e.preventDefault()
    try{
      await api.updateOrderStatus(oid, status)
      setMsg('Status updated')
      await load()
    }catch(e){ setMsg(e.message) }
  }

  if(!order) return <div className="p-6">Loading...</div>
  return (
    <div className="mx-auto max-w-4xl p-6">
      <h1 className="text-xl font-semibold">Order #{order.id}</h1>
      <div className="mt-4 rounded border bg-white p-4 shadow-sm">
        <div>Encounter: {order.encounter_id}</div>
        <div>Ordered By: {order.ordered_by}</div>
        <div>Placed At: {order.placed_at}</div>
        <div className="mt-2 flex items-center gap-2">
          <form onSubmit={updateStatus} className="flex items-center gap-2">
            <select className="rounded border p-1" value={status} onChange={(e)=>setStatus(e.target.value)}>
              {statuses.map(s => <option key={s} disabled={!allowedNext.includes(s)}>{s}</option>)}
            </select>
            <button className="rounded border px-3 py-1 hover:bg-gray-50" disabled={!allowedNext.includes(status)}>Update</button>
          </form>
          {msg && <span className="text-sm text-gray-600">{msg}</span>}
        </div>
        <div className="mt-2">Tests: {order.tests.join(', ')}</div>
      </div>

      <div className="mt-6 rounded border bg-white p-4 shadow-sm">
        <h2 className="font-medium">Results</h2>
        <ul className="mt-2 space-y-2 text-sm">
          {results.map(r => (
            <li key={r.id} className="rounded border p-2">
              <div>{r.test_code} = {r.value} {r.units || ''}</div>
              <div className="text-gray-500">Resulted: {r.resulted_at || r.received_at}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
