import { useState, useEffect } from 'react'
import './TopArtists.css'

function TopArtists() {
  const [artists, setArtists] = useState([])
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('medium_term')

  useEffect(() => {
    fetchArtists()
  }, [timeRange])

  const fetchArtists = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/top-artists?time_range=${timeRange}&limit=20`, {
        credentials: 'include'
      })
      if (response.ok) {
        const data = await response.json()
        setArtists(data.artists)
      }
    } catch (error) {
      console.error('Error fetching artists:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading your top artists...</div>
  }

  return (
    <div className="top-artists">
      <div className="section-header">
        <h2>Your Top Artists</h2>
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

      <div className="artists-grid">
        {artists.map((artist, index) => (
          <a
            key={artist.id}
            href={artist.external_url}
            target="_blank"
            rel="noopener noreferrer"
            className="artist-card"
            title={`Open ${artist.name} on Spotify`}
          >
            <div className="artist-rank">#{index + 1}</div>
            <img src={artist.image} alt={artist.name} className="artist-image" />
            <div className="artist-info">
              <h3 className="artist-name">{artist.name}</h3>
              <div className="artist-genres">
                {artist.genres.slice(0, 3).map((genre, i) => (
                  <span key={i} className="genre-tag">{genre}</span>
                ))}
              </div>
              <div className="artist-stats">
                <span className="stat">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                  </svg>
                  {artist.followers.toLocaleString()}
                </span>
                <span className="stat popularity">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  {artist.popularity}%
                </span>
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}

export default TopArtists
