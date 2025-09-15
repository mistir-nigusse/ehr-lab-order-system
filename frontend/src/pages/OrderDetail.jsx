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

  // New result state (LabTech only)
  const [testCode, setTestCode] = useState('')
  const [value, setValue] = useState('')
  const [units, setUnits] = useState('')
  const [addMsg, setAddMsg] = useState('')
  const [editRow, setEditRow] = useState(null)
  const [editValue, setEditValue] = useState('')
  const [editUnits, setEditUnits] = useState('')

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
        {roles.includes('LabTech') && (
          <form onSubmit={async (e)=>{e.preventDefault(); setAddMsg(''); try{ await api.createResults(oid, [{ test_code: testCode, value, units }]); setTestCode(''); setValue(''); setUnits(''); setAddMsg('Result added'); await load(); }catch(err){ setAddMsg(err.message||'Failed to add') } }} className="mt-3 grid grid-cols-4 gap-2">
            <input className="rounded border p-2" placeholder="Test code" value={testCode} onChange={(e)=>setTestCode(e.target.value)} required />
            <input className="rounded border p-2" placeholder="Value" value={value} onChange={(e)=>setValue(e.target.value)} required />
            <input className="rounded border p-2" placeholder="Units" value={units} onChange={(e)=>setUnits(e.target.value)} />
            <button className="rounded border px-3 py-1 hover:bg-gray-50">Add Result</button>
          </form>
        )}
        {addMsg && <div className="mt-1 text-sm text-gray-600">{addMsg}</div>}
        <ul className="mt-2 space-y-2 text-sm">
          {results.map(r => (
            <li key={r.id} className="rounded border p-2">
              {editRow === r.id && roles.includes('LabTech') ? (
                <div className="flex items-center gap-2">
                  <span className="text-gray-600">{r.test_code}</span>
                  <input className="rounded border p-1" value={editValue} onChange={(e)=>setEditValue(e.target.value)} placeholder="Value" />
                  <input className="rounded border p-1" value={editUnits} onChange={(e)=>setEditUnits(e.target.value)} placeholder="Units" />
                  <button className="rounded border px-2 py-1" onClick={async ()=>{ try{ await api.updateResult(oid, r.id, { value: editValue, units: editUnits }); setEditRow(null); await load(); }catch(e){ setMsg(e.message) } }}>Save</button>
                  <button className="rounded border px-2 py-1" onClick={()=>setEditRow(null)}>Cancel</button>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <div>
                    <div>{r.test_code} = {r.value} {r.units || ''}</div>
                    <div className="text-gray-500">Resulted: {r.resulted_at || r.received_at}</div>
                  </div>
                  {roles.includes('LabTech') && (
                    <div className="flex items-center gap-2">
                      <button className="rounded border px-2 py-1" onClick={()=>{ setEditRow(r.id); setEditValue(r.value || ''); setEditUnits(r.units || '') }}>Edit</button>
                      <button className="rounded border px-2 py-1" onClick={async ()=>{ if(confirm('Delete result?')){ try{ await api.deleteResult(oid, r.id); await load(); }catch(e){ setMsg(e.message) } } }}>Delete</button>
                    </div>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
