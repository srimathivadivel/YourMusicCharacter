from flask import Flask, jsonify, redirect, request, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import sqlite3
import logging
import time

# initializes Flask app and Session
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
session

# initializes SpotifyOAuth object with credentials and scope
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

# creates a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('characters.db')
    return conn

# Define character types and their associated genres
genre_file = open('genre_character_mapping.json')
CHARACTER_TYPES = json.load(genre_file)

# Function to set up the database
def setup_database():
    conn = create_connection()
    c = conn.cursor()

    # Drop the table if it exists to start fresh
    c.execute('DROP TABLE IF EXISTS characters')

    # Create the characters table
    c.execute('''
    CREATE TABLE characters
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    character_type TEXT NOT NULL)
    ''')

    # Add new sample data
    sample_data = [
        ('Rock Rebel', 'character1.png', 'Rocker'),
        ('Pop Princess', 'character2.png', 'Pop Star'),
        ('Soul Sister', 'character3.png', 'Soulful Singer'),
        ('Hip Hop Hero', 'character4.png', 'Hip Hop Artist'),
        ('Folk Troubadour', 'character5.png', 'Folk Musician')
    ]
    c.executemany('''
    INSERT INTO characters (name, image_url, character_type) VALUES (?, ?, ?)
    ''', sample_data)

    conn.commit()
    conn.close()

# calls setup_database at the start of the application
setup_database()

# classifies character based on genres
def classify_character(genres):
    scores = {character: 0 for character in CHARACTER_TYPES}
    print("asdf" + str(scores))

    for genre in genres:
        logging.debug(f"Processing genre: {genre}")
        for character, related_genres in CHARACTER_TYPES.items():
            if any(g in genre.lower() for g in related_genres):
                logging.debug(f"Matched genre '{genre}' with character '{character}'")
                scores[character] += 1

    if all(score == 0 for score in scores.values()):
        logging.debug("No matching genres found. Returning 'Unknown Artist'.")
        return "Unknown Artist"  # Default type if no match is found

    max_character = max(scores, key=scores.get)
    logging.debug(f"Classified character type: {max_character} with score {scores[max_character]}")
    return max_character

# retrieves a character from the database based on the genre
def get_character_by_genre(genre):
    logging.debug(f"Retrieving character for genre: {genre}")
    character_type = classify_character([genre])
    conn = create_connection()
    cursor = conn.cursor()
    
    if character_type == "Unknown Artist":
        logging.debug(f"Character type 'Unknown Artist' for genre '{genre}'")
        return ("Mystery Musician", "default_character.png"), character_type
    
    cursor.execute('''
    SELECT name, image_url FROM characters WHERE character_type = ? ORDER BY RANDOM() LIMIT 1
    ''', (character_type,))
    
    character = cursor.fetchone()
    conn.close()
    
    if character is None:
        logging.debug(f"No character found for type '{character_type}'. Returning default character.")
        return ("Mystery Musician", "default_character.png"), character_type
    
    logging.debug(f"Retrieved character '{character[0]}' with image URL '{character[1]}' for type '{character_type}'")
    return character, character_type

# retrieves the first genre of an artist
def get_genre_for_artist(artist_id, sp):
    artist = sp.artist(artist_id)
    if 'genres' in artist and len(artist['genres']) > 0:
        return artist['genres'][0]
    return None

@app.route('/')
def index():
    logging.debug("Rendering index.html")
    session.clear()
    return render_template('index.html')

@app.route('/login')
def login():
    # Deleting cache file if it exists to have most current data for current user
    cache_path = '.cache'
    if os.path.exists(cache_path):
        os.remove(cache_path)
    logging.debug("Redirecting to Spotify authorization URL.")
    auth_url = sp_oauth.get_authorize_url()
    logging.debug(f"Authorization URL: {auth_url}")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    logging.debug(f"Received authorization code: {code}")
    try:
        token_info = sp_oauth.get_access_token(code)
        logging.debug(f"Obtained token info: {token_info}")
    except Exception as e:
        logging.error(f"Error obtaining access token: {str(e)}")
        return jsonify(error="Error obtaining access token"), 500
    session['token_info'] = token_info
    return redirect(url_for('top_songs'))

@app.route('/top-songs')
def top_songs():
    token_info = get_token()
    if not token_info:
        logging.error("No token info available, redirecting to home.")
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    try:
        top_songs_data = sp.current_user_top_tracks(limit=5)
        logging.debug(f"Top songs data: {top_songs_data}")
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching top songs: {str(e)}")
        return render_template('top_songs.html', error=f"Error fetching top songs: {str(e)}")
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
    logging.debug(f"Tracks to be rendered: {tracks}")
    return render_template('top_songs.html', tracks=tracks)

@app.route('/character/<track_id>')
def character(track_id):
    token_info = get_token()
    if not token_info:
        logging.error("No token info available, redirecting to home.")
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    try:
        track = sp.track(track_id)
        genre = get_genre_for_artist(track['artists'][0]['id'], sp) or "Unknown Genre"
        (character_name, character_image_url), character_type = get_character_by_genre(genre)
        image_path = url_for('static', filename='characters/' + character_image_url)
        logging.debug(f"Track Name: {track['name']}, Character Name: {character_name}, Image URL: {character_image_url}, Character Type: {character_type}")
        logging.debug(f"Image Path: {image_path}")
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching character: {str(e)}")
        return render_template('character.html', 
                               track_name="Unknown Track", 
                               character_name="Error", 
                               character_image_url="error.png",
                               character_type="Error",
                               error=f"Error fetching character: {str(e)}")

    return render_template('character.html', 
                           track_name=track['name'], 
                           character_name=character_name, 
                           character_image_url=character_image_url,
                           character_type=character_type)

def check_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM characters')
    characters = cursor.fetchall()
    for character in characters:
        logging.debug(character)
    conn.close()

# calls check_database at the start of the application to debug
check_database()

# helper function to get or refresh the access token
def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        logging.error("No token_info found in session.")
        return None
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        logging.info("Token expired, refreshing...")
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            logging.debug(f"Refreshed token info: {token_info}")
        except Exception as e:
            logging.error(f"Error refreshing access token: {str(e)}")
            return None
        session['token_info'] = token_info
    return token_info

if __name__ == '__main__':
    app.run(debug=True)
