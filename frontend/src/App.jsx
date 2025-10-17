import { useState, useEffect } from 'react'
import './App.css'
import Login from './components/Login'
import Dashboard from './components/Dashboard'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check authentication status on load
    checkAuthStatus()

    // Check for callback success/error in URL
    const params = new URLSearchParams(window.location.search)
    if (params.get('success') === 'true') {
      setIsAuthenticated(true)
      window.history.replaceState({}, '', '/')
    } else if (params.get('error')) {
      console.error('Authentication error:', params.get('error'))
      window.history.replaceState({}, '', '/')
    }
  }, [])

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/api/auth-status', {
        credentials: 'include'
      })
      const data = await response.json()
      setIsAuthenticated(data.authenticated)
    } catch (error) {
      console.error('Error checking auth status:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading...</div>
      </div>
    )
  }

  return (
    <div className="app">
      {isAuthenticated ? <Dashboard />: <Login />}
    </div>
  )
}

export default App
