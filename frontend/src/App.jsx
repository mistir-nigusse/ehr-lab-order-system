import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import NavBar from './components/NavBar'
import Login from './pages/Login'
import Patients from './pages/Patients'
import PatientDetail from './pages/PatientDetail'
import OrderDetail from './pages/OrderDetail'
import Labs from './pages/Labs'
import { isAuthed } from './lib/auth.js'

function RequireAuth({ children }) {
  const loc = useLocation()
  if (!isAuthed()) return <Navigate to="/login" state={{ from: loc }} replace />
  return children
}

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <NavBar />
      <div className="mx-auto max-w-6xl p-6">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/patients" element={<RequireAuth><Patients /></RequireAuth>} />
          <Route path="/patients/:id" element={<RequireAuth><PatientDetail /></RequireAuth>} />
          <Route path="/orders/:id" element={<RequireAuth><OrderDetail /></RequireAuth>} />
          <Route path="/labs" element={<Labs />} />
          <Route path="/" element={<Navigate to="/patients" replace />} />
          <Route path="*" element={<div>Not Found</div>} />
        </Routes>
      </div>
    </div>
  )
}

export default App
