import { useState, useEffect } from 'react'
import './RecentTracks.css'

function RecentTracks() {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecentTracks()
  }, [])

  const fetchRecentTracks = async () => {
    try {
      const response = await fetch('/api/recent-tracks?limit=50', {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setTracks(data.tracks)
      }
    } catch (error) {
      console.error('Error fetching recent tracks:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatPlayedAt = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000)
    const seconds = ((ms % 60000) / 1000).toFixed(0)
    return `${minutes}:${seconds.padStart(2, '0')}`
  }

  if (loading) {
    return <div className="loading">Loading your recent tracks...</div>
  }

  return (
    <div className="recent-tracks">
      <div className="section-header">
        <h2>Recently Played</h2>
        <p className="section-subtitle">Your last 50 played tracks</p>
      </div>

      <div className="tracks-list">
        {tracks.map((track, index) => (
          <a
            key={`${track.id}-${index}`}
            href={track.external_url}
            target="_blank"
            rel="noopener noreferrer"
            className="recent-track-item"
            title={`Play ${track.name} on Spotify`}
          >
            <img src={track.image} alt={track.name} className="track-image" />
            <div className="track-details">
              <h3 className="track-name">{track.name}</h3>
              <p className="track-artist">{track.artist}</p>
              <p className="track-album">{track.album}</p>
            </div>
            <div className="track-meta">
              <span className="track-duration">{formatDuration(track.duration_ms)}</span>
              <span className="track-played-at">{formatPlayedAt(track.played_at)}</span>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}

export default RecentTracks
