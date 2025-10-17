from flask import Flask, request, jsonify, redirect, session, send_from_directory
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

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(64).hex())
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:5000'])

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:5000/api/callback/')

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
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

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
@app.route('/api/callback')
@app.route('/api/callback/')
def callback():
    try:
        code = request.args.get('code')
        error = request.args.get('error')

        if error:
            print(f"Spotify OAuth error: {error}")
            return redirect(f'/?error={error}')

        if not code:
            print("No authorization code received from Spotify")
            return redirect('/?error=no_code')

        session.clear()

        token_info = sp_oauth.get_access_token(code, check_cache=False)

        if not token_info:
            print("Failed to get token from Spotify")
            return redirect('/?error=no_token')

        session['token_info'] = token_info
        print("Successfully authenticated with Spotify!")
        return redirect('/?success=true')

    except Exception as e:
        print(f"Callback error occurred")
        return redirect('/?error=callback_error')

@app.route('/api/auth-status')
def auth_status():
    token_info = get_token()
    return jsonify({'authenticated': token_info is not None})

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
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'external_url': track['external_urls']['spotify']
            })
        
        return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations')
def get_recommendations():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401

        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Get seed tracks/artists from query params or use top items
        seed_tracks = request.args.get('seed_tracks', '').split(',') if request.args.get('seed_tracks') else []
        seed_artists = request.args.get('seed_artists', '').split(',') if request.args.get('seed_artists') else []
        seed_genres = request.args.get('seed_genres', '').split(',') if request.args.get('seed_genres') else []
        limit = int(request.args.get('limit', 20))

        # If no seeds provided, try to get top tracks or artists
        if not seed_tracks and not seed_artists and not seed_genres:
            # Try short term first
            top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')

            if top_tracks['items']:
                seed_tracks = [track['id'] for track in top_tracks['items'][:5]]
            else:
                # If no short term, try medium term
                top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
                if top_tracks['items']:
                    seed_tracks = [track['id'] for track in top_tracks['items'][:5]]
                else:
                    # If still no tracks, try top artists
                    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
                    if top_artists['items']:
                        seed_artists = [artist['id'] for artist in top_artists['items'][:5]]
                    else:
                        # Last resort: use popular genres
                        seed_genres = ['pop', 'rock', 'indie']

        # Filter out empty strings from seeds
        seed_tracks = [t for t in seed_tracks if t]
        seed_artists = [a for a in seed_artists if a]
        seed_genres = [g for g in seed_genres if g]

        # Make sure we have at least one seed
        if not seed_tracks and not seed_artists and not seed_genres:
            return jsonify({'error': 'Unable to generate recommendations. Please listen to more music on Spotify first!'}), 400

        # Get recommendations
        results = sp.recommendations(
            seed_tracks=seed_tracks[:5] if seed_tracks else None,
            seed_artists=seed_artists[:5] if seed_artists else None,
            seed_genres=seed_genres[:5] if seed_genres else None,
            limit=limit
        )

        recommendations = []
        for track in results['tracks']:
            recommendations.append({
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'external_url': track['external_urls']['spotify'],
                'preview_url': track.get('preview_url')
            })

        return jsonify({'recommendations': recommendations})
    except Exception as e:
        print(f"Recommendations error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/genre-seeds')
def get_genre_seeds():
    try:
        token_info = get_token()
        if not token_info:
            return jsonify({'error': 'User not authenticated'}), 401

        sp = spotipy.Spotify(auth=token_info['access_token'])
        genres = sp.recommendation_genre_seeds()

        return jsonify({'genres': genres['genres']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import logging
    from werkzeug.serving import run_simple

    # Suppress Flask/Werkzeug request logs
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    print("Starting Flask server on http://127.0.0.1:5000")
    print("Open http://127.0.0.1:5000 in your browser")
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=False)