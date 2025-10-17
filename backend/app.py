from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(64).hex())
CORS(app, supports_credentials=True)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'https://127.0.0.1:5000/callback/')

SCOPE = 'user-top-read user-read-recently-played user-library-read playlist-read-private'


sp_oauth =  SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE
    )

def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    now = int(datetime.now().timestamp())
    is_expired = token_info['expires_at'] - now < 60
    
    if is_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    
    return token_info

sp = Spotify(auth_manager = sp_oauth )

@app.route('/')
def index():
    return f'''
    <html>
    <head><title>Spotify Dashboard</title></head>
    <body>
        <h1>🎵 Spotify Dashboard API</h1>
        <p><strong>Status:</strong> Running ✅</p>
        <p><strong>Credentials:</strong> {"Configured ✅" if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET else "Missing ❌"}</p>
        
        <h2>Test the OAuth:</h2>
        <p><a href="/login" style="background: #1db954; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🎵 Login with Spotify</a></p>

    </body>
    </html>
    '''

@app.route('/debug')
def debug_info():
    return jsonify({
        'spotify_client_id_set': bool(SPOTIFY_CLIENT_ID),
        'spotify_client_secret_set': bool(SPOTIFY_CLIENT_SECRET),
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'scopes': SCOPE
    })

@app.route('/login')
def login():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return jsonify({
            'error': 'Spotify credentials not configured',
            'message': 'Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your .env file'
        }), 500
    
    try:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Redirecting to Spotify...")
        return redirect(auth_url)
    except Exception as e:
        print(f"Error creating Spotify OAuth: {e}")
        return jsonify({
            'error': f'OAuth setup error: {str(e)}',
            'client_id_set': bool(SPOTIFY_CLIENT_ID),
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'scope': SCOPE
        }), 500

@app.route('/callback')
@app.route('/callback/')
def callback():
    try:
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            print(f"Spotify OAuth error: {error}")
            return f'<h1>Spotify OAuth Error: {error}</h1><p><a href="/">Try again</a></p>'
        
        if not code:
            print("No authorization code received from Spotify")
            return '<h1>No authorization code received</h1><p><a href="/">Try again</a></p>'
        
        session.clear()
        
        print(f"Getting access token with code: {code}")
        token_info = sp_oauth.get_access_token(code)
        
        if not token_info:
            print("Failed to get token from Spotify")
            return '<h1>Failed to get token from Spotify</h1><p><a href="/">Try again</a></p>'
            
        session['token_info'] = token_info
        print("Successfully authenticated with Spotify!")
        return '<h1>✅ Success! Spotify Authentication Complete</h1><p>You can now test the API endpoints:</p><ul><li><a href="/api/user">Get User Info</a></li><li><a href="/api/top-tracks">Get Top Tracks</a></li><li><a href="/api/top-artists">Get Top Artists</a></li></ul>'
        
    except Exception as e:
        print(f"Callback error: {e}")

@app.route('/api/user')
def get_user():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = sp.current_user()
        
        return jsonify({
            'id': user['id'],
            'name': user['display_name'],
            'followers': user['followers']['total'],
            'image': user['images'][0]['url'] if user['images'] else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-tracks')
def get_top_tracks():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401
        
        time_range = request.args.get('time_range', 'medium_term') 
        limit = int(request.args.get('limit', 50))
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
        
        tracks = []
        for track in results['items']:
            tracks.append({
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'external_url': track['external_urls']['spotify']
            })
        
        return jsonify({'tracks': tracks, 'time_range': time_range})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-artists')
def get_top_artists():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401
        
        time_range = request.args.get('time_range', 'medium_term')
        limit = int(request.args.get('limit', 50))
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_top_artists(time_range=time_range, limit=limit)
        
        artists = []
        for artist in results['items']:
            artists.append({
                'id': artist['id'],
                'name': artist['name'],
                'genres': artist['genres'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'image': artist['images'][0]['url'] if artist['images'] else None,
                'external_url': artist['external_urls']['spotify']
            })
        
        return jsonify({'artists': artists, 'time_range': time_range})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent-tracks')
def get_recent_tracks():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401
        
        limit = int(request.args.get('limit', 50))
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_recently_played(limit=limit)
        
        tracks = []
        for item in results['items']:
            track = item['track']
            tracks.append({
                'played_at': item['played_at'],
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        print("Starting Flask server")
        print("Note: You'll see a browser security warning - click 'Advanced' -> 'Proceed to localhost (unsafe)'")
        app.run(debug=True, port=5000, ssl_context='adhoc', host='127.0.0.1')
    except ImportError as e:
        print(f"ERROR: Missing SSL dependency: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to start HTTPS server: {e}")
        exit(1)