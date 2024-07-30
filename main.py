import os
import time
from flask import Flask, redirect, request, session, url_for, jsonify, render_template, send_from_directory
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import logging
import sqlite3

# Initialize Flask app and Session
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ensure environment variables are set correctly
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID', '89574784a71644b4bf7f626ef4469f5f')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET', '7c29358ef6c6487cb8fd3e60b0be9cb1')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:5000/callback')

# Initialize SpotifyOAuth object with credentials and scope
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-top-read'
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# SQLite database connection
def create_connection():
    conn = sqlite3.connect('characters.db')
    return conn

# Retrieve a character based on genre from the database
def get_character_by_genre(genre):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name, image_url FROM characters WHERE genre = ? ORDER BY RANDOM() LIMIT 1
    ''', (genre,))
    character = cursor.fetchone()
    conn.close()
    return character

# Retrieve the genre for a given artist from Spotify
def get_genre_for_artist(artist_id, sp):
    artist = sp.artist(artist_id)
    if 'genres' in artist and len(artist['genres']) > 0:
        return artist['genres'][0]
    return None

# Render the homepage
@app.route('/')
def index():
    return render_template('homepage.html')

# Redirect to Spotify login
@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Callback endpoint after Spotify authentication
@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        return redirect(url_for('top_songs'))
    except spotipy.oauth2.SpotifyOauthError as e:
        logging.error(f"Error in OAuth callback: {str(e)}")
        return jsonify(error=f"Error in OAuth callback: {str(e)}"), 500

# Fetch top songs of the user
@app.route('/top-songs')
def top_songs():
    token_info = get_token()
    if not token_info:
        return redirect('/login')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    try:
        top_songs_data = sp.current_user_top_tracks(limit=5)
        logging.debug(f"Top songs data: {top_songs_data}")
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching top songs: {str(e)}")
        return jsonify(error=f"Error fetching top songs: {str(e)}"), 500

    tracks = []
    for track in top_songs_data['items']:
        genre = get_genre_for_artist(track['artists'][0]['id'], sp)
        tracks.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'genre': genre,
            'preview_url': track['preview_url']
        })

    return jsonify(tracks)

# Fetch character information based on track ID
@app.route('/character/<track_id>')
def character(track_id):
    token_info = get_token()
    if not token_info:
        return redirect('/login')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    try:
        track = sp.track(track_id)
        genre = get_genre_for_artist(track['artists'][0]['id'], sp)
        character = get_character_by_genre(genre)
        if character:
            character_name, character_image_url = character
        else:
            character_name = "No character found"
            character_image_url = ""
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching character: {str(e)}")
        return jsonify(error=f"Error fetching character: {str(e)}"), 500

    return jsonify({
        'track_name': track['name'],
        'character_name': character_name,
        'character_image_url': character_image_url
    })

# Retrieve access token from session, refresh if expired
def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    if is_expired:
        logging.info("Token expired, refreshing...")
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        except spotipy.oauth2.SpotifyOauthError as e:
            logging.error(f"Error refreshing access token: {str(e)}")
            return None

    return token_info

# Serve static assets from 'static/assets' directory
@app.route('/static/assets/<path:path>')
def send_assets(path):
    return send_from_directory('static/assets', path)

# Handle 404 errors
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
