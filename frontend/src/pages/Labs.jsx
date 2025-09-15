import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { getRoles } from '../lib/auth'

export default function Labs() {
  const [orders, setOrders] = useState([])
  const [msg, setMsg] = useState('')
  const nav = useNavigate()
  const roles = getRoles()

  useEffect(() => {
    if (!roles.includes('LabTech')) {
      setMsg('You are not authorized to view lab orders.')
      return
    }
    api.listLabOrders().then(setOrders).catch(e=>setMsg(e.message || 'Failed to load'))
  }, [])

  return (
    <div className="mx-auto max-w-5xl p-6">
      <h1 className="text-xl font-semibold">Lab Orders</h1>
      {msg && <div className="mt-2 text-sm text-gray-600">{msg}</div>}
      <div className="mt-4 overflow-x-auto rounded border bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-left">
            <tr>
              <th className="px-4 py-2">Order #</th>
              <th className="px-4 py-2">Encounter</th>
              <th className="px-4 py-2">Status</th>
              <th className="px-4 py-2">Tests</th>
              <th className="px-4 py-2">Placed</th>
              <th className="px-4 py-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.id} className="border-t">
                <td className="px-4 py-2">{o.id}</td>
                <td className="px-4 py-2">{o.encounter_id}</td>
                <td className="px-4 py-2">{o.status === 'in_progress' ? 'In Progress' : (o.status || '').charAt(0).toUpperCase() + (o.status || '').slice(1)}</td>
                <td className="px-4 py-2">{(o.tests||[]).join(', ')}</td>
                <td className="px-4 py-2">{o.placed_at}</td>
                <td className="px-4 py-2"><button className="rounded border px-2 py-1" onClick={()=>nav(`/orders/${o.id}`)}>Open</button></td>
              </tr>
            ))}
            {orders.length === 0 && (
              <tr><td className="px-4 py-3 text-gray-500" colSpan={6}>No orders for your lab.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
