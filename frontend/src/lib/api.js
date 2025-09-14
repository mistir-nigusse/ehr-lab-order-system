import { getToken, clearToken } from './auth.js'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'

async function request(path, { method = 'GET', body, headers = {}, auth = true } = {}) {
  const h = { 'Content-Type': 'application/json', ...headers }
  if (auth) {
    const token = getToken()
    if (token) h['Authorization'] = `Bearer ${token}`
  }
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: h,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (res.status === 401) {
    clearToken()
    throw new Error('Unauthorized')
  }
  const ct = res.headers.get('content-type') || ''
  const data = ct.includes('application/json') ? await res.json() : await res.text()
  if (!res.ok) {
    const msg = (data && data.error) || res.statusText
    const err = new Error(msg)
    err.status = res.status
    err.data = data
    throw err
  }
  return data
}

export const api = {
  login: (username, password, role) => request('/api/auth/login', { method: 'POST', body: { username, password, role }, auth: false }),

  // Patients
  createPatient: (p) => request('/api/patients', { method: 'POST', body: p }),
  searchPatients: (q) => request(`/api/patients/search?q=${encodeURIComponent(q)}`),
  getPatientSummary: (id) => request(`/api/patients/${id}/summary`),

  // EHR
  createEncounter: (payload) => request('/api/encounters', { method: 'POST', body: payload }),
  appendNote: (payload) => request('/api/ehr/notes', { method: 'POST', body: payload }),
  addProblem: (payload) => request('/api/ehr/problems', { method: 'POST', body: payload }),
  addAllergy: (payload) => request('/api/ehr/allergies', { method: 'POST', body: payload }),
  addMedication: (payload) => request('/api/ehr/medications', { method: 'POST', body: payload }),

  // Orders
  placeOrder: (payload) => request('/api/orders/lab', { method: 'POST', body: payload }),
  getOrder: (id) => request(`/api/orders/lab/${id}`),
  updateOrderStatus: (id, status) => request(`/api/orders/lab/${id}/status`, { method: 'PATCH', body: { status } }),

  // Labs
  postResults: (payload, secret) => request('/api/labs/results', { method: 'POST', body: payload, headers: secret ? { 'X-Labs-Secret': secret } : {} , auth: false }),
}

export { API_BASE }
