from flask import Flask, redirect, request, session, url_for, render_template
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
CHARACTER_TYPES = {
  "Rocker": [
    "rock", "metal", "punk", "grunge", "alternative rock", "hard rock",
    "heavy metal", "classic rock", "garage rock", "punk rock",
    "progressive rock", "blues rock", "glam rock", "psychedelic rock",
    "indie rock", "arena rock", "stoner rock", "post-punk", "goth rock",
    "doom metal", "black metal", "death metal", "nu metal", "thrash metal",
    "speed metal", "sludge metal", "power metal", "symphonic metal", 
    "folk metal", "viking metal", "hardcore punk", "emo", "ska punk",
    "crust punk", "industrial rock", "math rock", "shoegaze", "noise rock",
    "funk rock", "rap rock", "alt-metal", "art rock", "avant-garde metal",
    "crossover thrash", "deathcore", "grindcore", "metalcore", "post-metal",
    "space rock", "southern rock", "psychedelic metal", "gothic metal", 
    "progressive metal", "technical death metal", "melodic death metal", 
    "blackened death metal", "groove metal", "drone metal", "industrial metal",
    "nu-gaze", "post-rock", "jangle pop", "krautrock", "britpop", 
    "garage punk", "horror punk", "new wave of british heavy metal", 
    "visual kei", "j-rock", "k-rock", "glam metal", "sleaze rock", 
    "arena rock", "death-doom", "funeral doom", "blackened doom", 
    "stoner doom", "post-black metal", "ambient black metal", 
    "melodic black metal", "symphonic black metal", "technical metal", 
    "djent", "cyber metal", "nu-core", "rapcore", "folk punk", 
    "gypsy punk", "psychobilly", "horror punk", "deathrock", 
    "coldwave", "darkwave", "minimal wave", "gothic rock", 
    "ethereal wave", "neofolk", "apocalyptic folk", "martial industrial",
    "dark ambient", "dark folk", "space metal"
  ],
  "Pop Star": [
    "pop", "dance", "electronic", "synthpop", "electropop", "dance-pop",
    "k-pop", "j-pop", "teen pop", "indie pop", "bubblegum pop",
    "art pop", "hyperpop", "latin pop", "pop rock", "europop",
    "futurepop", "pop rap", "pop punk", "disco", "house",
    "trance", "techno", "ambient", "chillwave", "dream pop",
    "new wave", "progressive pop", "tropical house", "deep house", 
    "eurodance", "dancehall", "synthwave", "future bass", "vaporwave",
    "electro house", "progressive house", "big room house", "trap",
    "twerk", "moombahton", "future house", "bass house", "garage",
    "dubstep", "drum and bass", "glitch hop", "jungle", "hardcore",
    "breakbeat", "electroclash", "italo disco", "nu-disco", 
    "chiptune", "bitpop", "j-pop", "idol pop", "city pop", 
    "shibuya-kei", "enka", "visual kei", "anime pop", 
    "bubblegum dance", "scandipop", "eurobeat", "italodance", 
    "hands up", "hi-nrg", "commercial dance", "progressive trance",
    "uplifting trance", "goa trance", "psytrance", "hard trance", 
    "chillstep", "liquid funk", "neurofunk", "jump up", 
    "jungle terror", "bassline", "speed garage", "uk garage", 
    "future garage", "2-step", "grime", "dark pop", "electro swing",
    "b-more", "future bounce", "deep pop", "tropical pop", "melodic house"
  ],
  "Soulful Singer": [
    "r&b", "soul", "jazz", "blues", "neo-soul", "funk", "motown",
    "smooth jazz", "contemporary r&b", "swing", "bebop", "vocal jazz",
    "gospel", "doo-wop", "blue-eyed soul", "acid jazz", "fusion",
    "jazz funk", "blues rock", "ragtime", "new jack swing", "quiet storm",
    "philly soul", "northern soul", "southern soul", "psychedelic soul",
    "urban contemporary", "boogie", "afrobeat", "latin jazz", "soul jazz",
    "gypsy jazz", "bossa nova", "cool jazz", "free jazz", "post-bop",
    "hard bop", "soul blues", "smooth soul", "progressive soul", "nu jazz",
    "avant-garde jazz", "contemporary jazz", "traditional jazz", "electro swing",
    "jazz fusion", "ethio-jazz", "jazz rap", "mambo", "salsa", "samba",
    "tango", "cha-cha-cha", "reggaeton", "bachata", "merengue", 
    "flamenco", "timba", "son cubano", "bolero", "boogaloo", 
    "bossa nova", "tropicalia", "mariachi", "ranchera", "norteño", 
    "tejano", "cumbia", "vallenato", "soca", "calypso", "ska", 
    "rocksteady", "reggae", "dancehall", "lovers rock", "dub", 
    "reggae fusion", "roots reggae", "mento", "zydeco", "cajun", 
    "swamp pop", "gospel blues", "spirituals", "hymns", "bluegrass gospel", 
    "quartet gospel", "sacred steel", "christian soul", "urban gospel",
    "country gospel", "southern gospel", "black gospel", "contemporary christian"
  ],
  "Hip Hop Artist": [
    "hip hop", "rap", "trap", "grime", "boom bap", "gangsta rap",
    "east coast hip hop", "west coast hip hop", "southern hip hop",
    "conscious hip hop", "crunk", "drill", "mumble rap", "old school hip hop",
    "underground hip hop", "trap soul", "alternative hip hop", "reggaeton",
    "hyphy", "cloud rap", "trap metal", "emo rap", "latin trap", "afro trap",
    "chopped and screwed", "dirty south", "g-funk", "hardcore hip hop", 
    "jazz rap", "miami bass", "nerdcore", "turntablism", "hyphy", "snap music",
    "phonk", "bounce", "drill", "grime", "trap rap", "trap soul", "industrial hip hop",
    "conscious hip hop", "east coast rap", "west coast rap", "southern rap", "nuyorican rap",
    "reggae fusion", "reggae rap", "dancehall", "ragga", "bashment",
    "baile funk", "funk carioca", "favela funk", "bhangra", "desi hip hop",
    "k-hip hop", "j-hip hop", "euro-rap", "francophone rap", "british hip hop",
    "aussie hip hop", "drill", "uk drill", "chicago drill", "brooklyn drill",
    "trap drill", "bounce music", "crunkcore", "crunk", "memphis rap",
    "new jack swing", "ragga hip hop", "trip hop", "abstract hip hop",
    "neo-soul", "conscious rap", "latin hip hop", "spanish hip hop", "turkish hip hop",
    "german hip hop", "french hip hop", "italian hip hop", "portuguese hip hop",
    "afrobeats", "afroswing", "britfunk", "dembow", "trapeton", "trance hop",
    "raggatek", "rap rock", "rap metal", "rapcore", "horrorcore", "juggalo", 
    "queercore", "psychedelic hip hop", "rap opera", "rap musical",
    "kentucky hip hop", "memphis hip hop", "brooklyn drill", "florida drill", "canadian hip hop"
  ],
  "Folk Musician": [
    "folk", "country", "acoustic", "indie", "bluegrass", "americana",
    "alt-country", "singer-songwriter", "traditional folk", "celtic",
    "appalachian", "roots rock", "folk rock", "new acoustic", "folk pop",
    "indie folk", "country rock", "outlaw country", "cowboy", "gospel",
    "folk punk", "neofolk", "cajun", "zydeco", "contemporary folk",
    "british folk", "irish folk", "scottish folk", "canadian folk", 
    "protest folk", "traditional country", "western swing", "cowpunk", 
    "folk metal", "americana", "bluegrass gospel", "new country",
    "celtic rock", "celtic punk", "progressive folk", "world folk", 
    "freak folk", "psych folk", "urban folk", "country folk", 
    "folk blues", "folk jazz", "folk baroque", "ethereal folk",
    "electric folk", "folk revival", "appalachian folk", "contemporary folk",
    "folk rap", "folk pop", "celtic folk", "bluegrass", "newgrass", 
    "mountain music", "bluegrass gospel", "progressive bluegrass", 
    "roots revival", "folk dance", "balfolk", "folk rock", "folk punk", 
    "indie folk", "nu-folk", "anti-folk", "progressive folk", "freak folk", 
    "psych folk", "urban folk", "traditional folk", "neotraditional folk",
    "acoustic folk", "chamber folk", "contemporary folk", "electro-folk",
    "folk-pop", "folk-metal", "folk-punk", "folk-rock", "folk-soul",
    "folk-tronica", "psychedelic folk", "world folk", "folk rap",
    "folk jazz", "folk blues", "folk funk", "folk gospel", "indie folk",
    "new folk", "neo-folk", "post-folk", "proto-folk"
  ]
}

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
    genres = []
    for track in top_songs_data['items']:
        genre = get_genre_for_artist(track['artists'][0]['id'], sp)
        if genre:
            genres.append(genre)
        tracks.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'genre': genre,
            'preview_url': track['preview_url']
        })
    logging.debug(f"Tracks to be rendered: {tracks}")
    session['genres'] = genres  # Store genres in session
    return render_template('top_songs.html', tracks=tracks)

@app.route('/discover-character')
def discover_character():
    genres = session.get('genres', [])
    if not genres:
        logging.error("No genres found in session.")
        return redirect('/')
    
    logging.debug(f"Processing genres for character classification: {genres}")
    character_type = classify_character(genres)
    (character_name, character_image_url), character_type = get_character_by_genre(character_type)
    image_path = url_for('static', filename='characters/' + character_image_url)
    
    logging.debug(f"Character Name: {character_name}, Image URL: {character_image_url}, Character Type: {character_type}")
    logging.debug(f"Image Path: {image_path}")
    
    return render_template('character.html', 
                           track_name="Your Top 5 Songs", 
                           character_name=character_name, 
                           character_image_url=character_image_url,
                           character_type=character_type)

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
