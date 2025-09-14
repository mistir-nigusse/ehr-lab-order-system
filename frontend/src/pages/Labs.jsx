import { useState } from 'react'
import { api } from '../lib/api'

export default function Labs() {
  const [orderId, setOrderId] = useState('')
  const [payload, setPayload] = useState('[{"test_code":"A1C","value":"5.7","units":"%"}]')
  const [secret, setSecret] = useState('')
  const [msg, setMsg] = useState('')

  async function submit(e){
    e.preventDefault()
    setMsg('')
    try{
      const results = JSON.parse(payload)
      await api.postResults({ orderId: Number(orderId), results }, secret)
      setMsg('Results accepted')
    }catch(err){ setMsg(err.message || 'Failed to post results') }
  }

  return (
    <div className="mx-auto max-w-3xl p-6">
      <h1 className="text-xl font-semibold">Labs (Dev)</h1>
      <form onSubmit={submit} className="mt-4 space-y-3">
        <div>
          <label className="block text-sm text-gray-700">Order ID</label>
          <input className="mt-1 w-full rounded border p-2" value={orderId} onChange={(e)=>setOrderId(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm text-gray-700">Results JSON (array of objects)</label>
          <textarea rows={6} className="mt-1 w-full rounded border p-2" value={payload} onChange={(e)=>setPayload(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm text-gray-700">X-Labs-Secret (optional)</label>
          <input className="mt-1 w-full rounded border p-2" value={secret} onChange={(e)=>setSecret(e.target.value)} />
        </div>
        <button className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">Submit Results</button>
        {msg && <div className="text-sm text-gray-600">{msg}</div>}
      </form>
    </div>
  )
}

