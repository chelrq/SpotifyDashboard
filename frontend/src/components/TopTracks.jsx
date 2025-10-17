import { useState, useEffect } from 'react'
import './TopTracks.css'

function TopTracks() {
  const [tracks, setTracks] = useState([])
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('medium_term')

  useEffect(() => {
    fetchTracks()
  }, [timeRange])

  const fetchTracks = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/top-tracks?time_range=${timeRange}&limit=20`, {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setTracks(data.tracks)
      }
    } catch (error) {
      console.error('Error fetching tracks:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDuration = (ms) => {
    const minutes = Math.floor(ms / 60000)
    const seconds = ((ms % 60000) / 1000).toFixed(0)
    return `${minutes}:${seconds.padStart(2, '0')}`
  }

  if (loading) {
    return <div className="loading">Loading your top tracks...</div>
  }

  return (
    <div className="top-tracks">
      <div className="section-header">
        <h2>Your Top Tracks</h2>
        <div className="time-range-selector">
          <button
            className={timeRange === 'short_term' ? 'active' : ''}
            onClick={() => setTimeRange('short_term')}
          >
            Last 4 Weeks
          </button>
          <button
            className={timeRange === 'medium_term' ? 'active' : ''}
            onClick={() => setTimeRange('medium_term')}
          >
            Last 6 Months
          </button>
          <button
            className={timeRange === 'long_term' ? 'active' : ''}
            onClick={() => setTimeRange('long_term')}
          >
            All Time
          </button>
        </div>
      </div>

      <div className="tracks-grid">
        {tracks.map((track, index) => (
          <a
            key={track.id}
            href={track.external_url}
            target="_blank"
            rel="noopener noreferrer"
            className="track-card"
            title={`Play ${track.name} on Spotify`}
          >
            <div className="track-rank">#{index + 1}</div>
            <img src={track.image} alt={track.name} className="track-image" />
            <div className="track-info">
              <h3 className="track-name">{track.name}</h3>
              <p className="track-artist">{track.artist}</p>
              <p className="track-album">{track.album}</p>
            </div>
            <div className="track-meta">
              <span className="track-duration">{formatDuration(track.duration_ms)}</span>
              <span className="track-popularity">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                {track.popularity}%
              </span>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}

export default TopTracks
