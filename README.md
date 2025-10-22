# Music Dashboard

A web application that creates personalized analytics dashboards for Spotify users, showing their top songs, top artists, and other analytics.

> ⚠️ This project is not affiliated with or endorsed by Spotify. It is for educational and personal use only.

## Tech Stack

### Backend
- **Spotify Web API**: https://developer.spotify.com/documentation/web-api/
- **Python Flask**: Web server and API endpoints
- **Spotipy**: Spotify Web API integration
- **Pandas**: Data analysis and processing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: User interface framework
- **Vite**: Build tool and development server
- **CSS3**: Responsive styling with modern design

## Prerequisites

- Python 3.8+
- Node.js 16+

## Features

- Spotify OAuth authentication
- User profile display with follower count
- Top Tracks (different time periods)
- Top Artists with genres and statistics
- Recently Played tracks with timestamps
- Responsive design for mobile and desktop

## Setup Instructions

### 1. Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Add `http://127.0.0.1:5000/api/callback/` to Redirect URIs in your dashboard settings
4. Save your `Client ID` and `Client Secret`
5. Adding any other users require manual set up in User Management tab

### 2. Environment Setup

Create a `.env` file in the `backend` directory with your Spotify credentials:

```bash
cp .env.example .env
```

Input your client id and secret here

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run build
```

### 5. Run the Application

Start the Flask server (which serves both backend API and frontend):

```bash
cd backend
python app.py
```

Visit `http://127.0.0.1:5000` in your browser and click "Connect with Spotify" to start!

## Development Mode

If you want to develop the frontend with hot-reload:

1. In one terminal, start the backend:
   ```bash
   cd backend
   python app.py
   ```

2. In another terminal, start the frontend dev server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Visit the frontend dev server URL 

Note: The Vite dev server proxies API requests to the backend at `http://127.0.0.1:5000`

## Project Structure

```
SpotifyDashboard/
├── backend/
│   ├── app.py              # Flask server and API endpoints
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── UserProfile.jsx
│   │   │   ├── TopTracks.jsx
│   │   │   ├── TopArtists.jsx
│   │   │   └── RecentTracks.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── dist/               # Built frontend (served by Flask)
│   └── package.json
└── README.md
```

## API Endpoints

- `GET /` - Serves the React frontend
- `GET /login` - Initiates Spotify OAuth flow
- `GET /callback` or `GET /api/callback` - OAuth callback endpoint
- `GET /api/auth-status` - Check if user is authenticated
- `GET /api/user` - Get current user profile
- `GET /api/top-tracks?time_range=medium_term&limit=50` - Get user's top tracks
- `GET /api/top-artists?time_range=medium_term&limit=50` - Get user's top artists
- `GET /api/recent-tracks?limit=50` - Get recently played tracks

## Future Plans

- Changing top limits (currently 20)
- Adding recommendation API calls
- Data dashboard with more statistics 
   - Requires manual download via `https://www.spotify.com/us/account/privacy/`
   - Requires additional wait time 

## License

This project is licensed under the GNU License - see the LICENSE file for details.
