import { useState, useEffect } from 'react'
import './Dashboard.css'
import UserProfile from './UserProfile'
import TopTracks from './TopTracks'
import TopArtists from './TopArtists'
import RecentTracks from './RecentTracks'

function Dashboard() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('tracks')

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const response = await fetch('/api/user', {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setUser(data)
      }
    } catch (error) {
      console.error('Error fetching user data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading your dashboard...</div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Spotify Dashboard</h1>
          {user && <UserProfile user={user} />}
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={`nav-button ${activeTab === 'tracks' ? 'active' : ''}`}
          onClick={() => setActiveTab('tracks')}
        >
          Top Tracks
        </button>
        <button
          className={`nav-button ${activeTab === 'artists' ? 'active' : ''}`}
          onClick={() => setActiveTab('artists')}
        >
          Top Artists
        </button>
        <button
          className={`nav-button ${activeTab === 'recent' ? 'active' : ''}`}
          onClick={() => setActiveTab('recent')}
        >
          Recent Plays
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'tracks' && <TopTracks />}
        {activeTab === 'artists' && <TopArtists />}
        {activeTab === 'recent' && <RecentTracks />}
      </main>
    </div>
  )
}

export default Dashboard
