function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="mx-auto max-w-5xl p-6">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold">EHR Lab Order System</h1>
          <nav className="flex gap-4 text-sm">
            <span className="text-gray-700">Patients</span>
            <span className="text-gray-500">EHR</span>
            <span className="text-gray-500">Orders</span>
            <span className="text-gray-500">Labs</span>
          </nav>
        </header>

        <section className="mt-8 grid gap-6 md:grid-cols-2">
          <div className="rounded-lg border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-medium">Patients</h2>
            <p className="mt-1 text-sm text-gray-600">Create, find, and manage patient records.</p>
            <div className="mt-4 flex gap-3">
              <button disabled className="cursor-not-allowed rounded bg-blue-200 px-4 py-2 text-white">Create Patient</button>
              <button disabled className="cursor-not-allowed rounded border border-gray-200 px-4 py-2 text-gray-500">Search</button>
            </div>
          </div>

          <div className="rounded-lg border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-medium">EHR</h2>
            <p className="mt-1 text-sm text-gray-600">Encounters, notes (append-only), problems, allergies, meds.</p>
            <div className="mt-4">
              <button disabled className="cursor-not-allowed rounded border border-gray-200 px-4 py-2 text-gray-500">Add Note</button>
            </div>
          </div>

          <div className="rounded-lg border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-medium">Orders</h2>
            <p className="mt-1 text-sm text-gray-600">Place and track lab orders through lifecycle.</p>
            <div className="mt-4">
              <button disabled className="cursor-not-allowed rounded border border-gray-200 px-4 py-2 text-gray-500">Place Lab Order</button>
            </div>
          </div>

          <div className="rounded-lg border bg-white p-5 shadow-sm">
            <h2 className="text-lg font-medium">Labs</h2>
            <p className="mt-1 text-sm text-gray-600">Accept lab results and integrate back to chart.</p>
            <div className="mt-4">
              <button disabled className="cursor-not-allowed rounded border border-gray-200 px-4 py-2 text-gray-500">Post Results</button>
            </div>
          </div>
        </section>

        <footer className="mt-10 text-center text-xs text-gray-500">Skeleton stage — features not implemented yet.</footer>
      </div>
    </div>
  )
}

export default App
