import os
import time
from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import logging
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Set your client ID, client secret, and redirect URI
SPOTIPY_CLIENT_ID = '9aea5dd3de9944b79791422c76a54cea'
SPOTIPY_CLIENT_SECRET = 'dc658f04cde94635a1ab70675916921e'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-top-read'
)

logging.basicConfig(level=logging.DEBUG)

def create_connection():
    conn = sqlite3.connect('characters.db')
    return conn

def get_character_by_genre(genre):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name, image_url FROM characters WHERE genre = ? ORDER BY RANDOM() LIMIT 1
    ''', (genre,))
    
    character = cursor.fetchone()
    conn.close()
    return character

def get_genre_for_artist(artist_id, sp):
    artist = sp.artist(artist_id)
    if 'genres' in artist and len(artist['genres']) > 0:
        return artist['genres'][0]  # Take the first genre
    return None

@app.route('/')
def index():
    session.clear()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('top_songs'))

@app.route('/top-songs')
def top_songs():
    token_info = get_token()
    if not token_info:
        return redirect('/')
    
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

    return render_template('top_songs.html', tracks=tracks)

@app.route('/character/<track_id>')
def character(track_id):
    token_info = get_token()
    if not token_info:
        return redirect('/')
    
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

    return render_template('character.html', track_name=track['name'], character_name=character_name, character_image_url=character_image_url)

def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        logging.info("Token expired, refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    return token_info

if __name__ == '__main__':
    app.run(debug=True)
