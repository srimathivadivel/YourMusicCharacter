import os
import time
from flask import Flask, redirect, request, session, url_for, render_template, jsonify
from flask_session import Session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import logging
import sqlite3

# Initialize Flask app and Session
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for the Flask app
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the filesystem
Session(app)

# Set Spotify API credentials and redirect URI
SPOTIPY_CLIENT_ID = '9aea5dd3de9944b79791422c76a54cea'
SPOTIPY_CLIENT_SECRET = 'dc658f04cde94635a1ab70675916921e'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback'

# Initialize SpotifyOAuth object with credentials and scope
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-top-read'  # Request 'user-top-read' scope to access user's top tracks
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Configure logging to print debug-level logs

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('characters.db')  # Connect to the 'characters.db' SQLite database
    return conn

# Function to retrieve a random character from the database based on the genre
def get_character_by_genre(genre):
    conn = create_connection()
    cursor = conn.cursor()

    # Execute a SQL query to select a random character with the given genre
    cursor.execute('''
    SELECT name, image_url FROM characters WHERE genre = ? ORDER BY RANDOM() LIMIT 1
    ''', (genre,))
    
    character = cursor.fetchone()  # Fetch the first (and only) result
    conn.close()
    return character  # Return the character name and image URL

# Function to retrieve the first genre of an artist
def get_genre_for_artist(artist_id, sp):
    artist = sp.artist(artist_id)  # Fetch artist information from the Spotify API
    if 'genres' in artist and len(artist['genres']) > 0:
        return artist['genres'][0]  # Return the first genre associated with the artist
    return None  # Return None if no genre is available

# Route for the index page, redirects to Spotify authorization URL
@app.route('/')
def index():
    session.clear()  # Clear the session data
    auth_url = sp_oauth.get_authorize_url()  # Get the Spotify authorization URL
    return redirect(auth_url)  # Redirect the user to the authorization URL

# Route for the callback URL after Spotify authorization
@app.route('/callback')
def callback():
    session.clear()  # Clear the session data
    code = request.args.get('code')  # Get the authorization code from the URL query parameters
    token_info = sp_oauth.get_access_token(code)  # Exchange the authorization code for an access token
    session['token_info'] = token_info  # Store the token information in the session
    return redirect(url_for('top_songs'))  # Redirect the user to the '/top-songs' route

# Route for displaying the user's top songs
@app.route('/top-songs')
def top_songs():
    token_info = get_token()  # Get the access token from the session
    if not token_info:
        return redirect('/')  # Redirect to the index page if no token is available

    sp = spotipy.Spotify(auth=token_info['access_token'])  # Create a Spotify client with the access token

    try:
        top_songs_data = sp.current_user_top_tracks(limit=5)  # Fetch the user's top 5 tracks
        logging.debug(f"Top songs data: {top_songs_data}")  # Log the top songs data
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching top songs: {str(e)}")  # Log any errors
        return jsonify(error=f"Error fetching top songs: {str(e)}"), 500  # Return an error response

    tracks = []
    for track in top_songs_data['items']:
        genre = get_genre_for_artist(track['artists'][0]['id'], sp)  # Get the first genre for the track's artist
        tracks.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'genre': genre,
            'preview_url': track['preview_url']
        })

    return render_template('top_songs.html', tracks=tracks)  # Render the 'top_songs.html' template with the track data

# Route for displaying a character based on the selected track's genre
@app.route('/character/<track_id>')
def character(track_id):
    token_info = get_token()  # Get the access token from the session
    if not token_info:
        return redirect('/')  # Redirect to the index page if no token is available

    sp = spotipy.Spotify(auth=token_info['access_token'])  # Create a Spotify client with the access token

    try:
        track = sp.track(track_id)  # Fetch the track information from the Spotify API
        genre = get_genre_for_artist(track['artists'][0]['id'], sp)  # Get the first genre for the track's artist
        character = get_character_by_genre(genre)  # Get a random character with the same genre
        if character:
            character_name, character_image_url = character
        else:
            character_name = "No character found"
            character_image_url = ""
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Error fetching character: {str(e)}")  # Log any errors
        return jsonify(error=f"Error fetching character: {str(e)}"), 500  # Return an error response

    # Render the 'character.html' template with the track name and character information
    return render_template('character.html', track_name=track['name'], character_name=character_name, character_image_url=character_image_url)

# Helper function to get or refresh the access token
def get_token():
    token_info = session.get('token_info', None)  # Get the token information from the session
    if not token_info:
        return None  # Return None if no token information is available

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60  # Check if the token is about to expire in less than 60 seconds

    if is_expired:
        logging.info("Token expired, refreshing...")  # Log that the token is being refreshed
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])  # Refresh the access token
        session['token_info'] = token_info  # Store the new token information in the session

    return token_info  # Return the token information

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)