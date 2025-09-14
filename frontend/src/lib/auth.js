const TOKEN_KEY = 'ehr.jwt'
const USER_KEY = 'ehr.user'

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || ''
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export function isAuthed() {
  return !!getToken()
}

export function setUser(user) {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify(user || {}))
  } catch {}
}

export function getUser() {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function getRoles() {
  const u = getUser()
  return (u && Array.isArray(u.roles)) ? u.roles : []
}
