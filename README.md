# Spotify Dashboard

A web application that creates personalized analytics dashboards for Spotify users, showing their most listened to songs, total listening time, top artists, and other analytics.

## Tech Stack

### Backend
- **Python Flask**: Web server and API endpoints
- **Spotipy**: Spotify Web API integration
- **Pandas**: Data analysis and processing
- **SQLite**: Database for caching user data
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: User interface framework
- **Vite**: Build tool and development server
- **CSS3**: Responsive styling with modern design

## Prerequisites

- Python 3.8+
- Node.js 16+

## Setup Instructions

1. Spotify API Setup
   1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   2. Create a new app
   3. Add `https://127.0.0.1:5000/callback/` to Redirect URIs in your dashboard
   4. Save your `Client ID` and `Client Secret`

2. Env Setup
   1. Create environment file:
      ```bash
      cp .env.example .env
      ```

   2. Edit `.env` with your Spotify credentials:
      ```
      SPOTIFY_CLIENT_ID=your_spotify_client_id_here
      SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
      ```

3. Backend Setup
   1. Navigate to the backend directory:
      ```bash
      cd backend
      ```

   2. Install Python dependencies:
      ```bash
      pip install -r requirements.txt
      ```

   3. Start the Flask server:
      ```bash
      python app.py
      ```

4. Frontend Setup
   1. Install Node.js dependencies:
      ```bash
      npm install
      ```

   2. Start the development server:
      ```bash
      npm run dev
      ```

5. Visit https://127.0.0.1:5000
6. Login to Spotify (doesn't have to match developer account)
7. Redirects to web app with data dashboard!


## License

This project is licensed under the MIT License - see the LICENSE file for details.
