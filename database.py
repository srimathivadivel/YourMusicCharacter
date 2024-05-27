import sqlite3

def create_connection():
    conn = sqlite3.connect('characters.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        artist TEXT,
        image_url TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_character(name, genre, artist, image_url):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO characters (name, genre, artist, image_url)
    VALUES (?, ?, ?, ?)
    ''', (name, genre, artist, image_url))
    
    conn.commit()
    conn.close()

def get_character_by_genre(genre):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name, image_url FROM characters WHERE genre = ? ORDER BY RANDOM() LIMIT 1
    ''', (genre,))
    
    character = cursor.fetchone()
    conn.close()
    return character

# Create the table
create_table()

# Example usage to insert characters
insert_character('Character 1', 'Pop', 'Taylor Swift', 'https://en.wikipedia.org/wiki/Ariel_%28The_Little_Mermaid%29#/media/File:Ariel_disney.png')
insert_character('Character 2', 'Rock', 'The Rolling Stones', 'd51mmvh-f906170b-a3ed-4002-9ade-7b1ee7542c42-1.png')
insert_character('Character 3', 'Hip Hop', 'Kendrick Lamar', '16-facts-about-penny-proud-the-proud-family-1693474715.jpg')
insert_character('Character 4', 'Jazz', 'Miles Davis', 'baloo-104035.jpg')
insert_character('Character 5', 'Classical', 'Ludovico Einaudi', 'Ludwig_Von_Drake_Duckipedia.png')
insert_character('Character 6', 'R&B', 'Beyoncé', 'Tiana_Disney.png')
insert_character('Character 7', 'Country', 'Luke Bryan', 'download.png')
insert_character('Character 8', 'Electronic', 'Calvin Harris', 'rb4i4BX5_400x400.jpg')
insert_character('Character 9', 'Reggae', 'Bob Marley', 'main-qimg-dc93ac4c71907a7ee2c579bcf6846af4.jpg')
insert_character('Character 10', 'Blues', 'B.B. King', '800px-0052Meowth.png')
insert_character('Character 11', 'Latin', 'Shakira', '15-facts-about-yzma-the-emperors-new-groove-1692276725.jpg')
insert_character('Character 12', 'Metal', 'Metallica', 'hShredder_(1987_animated_character_design).png')
insert_character('Character 13', 'Soul', 'Aretha Franklin', 'http://example.com/image13.jpg')
insert_character('Character 14', 'Folk', 'Bob Dylan', 'Mulan_disney.png')
insert_character('Character 15', 'Disco', 'Donna Summer', 'powerline-from-a-goofy-movie.jpg')
insert_character('Character 16', 'Punk', 'The Ramones', '9f555a86a0d293c82e0906581e4ff65e.jpg')
insert_character('Character 17', 'Funk', 'James Brown', 'Marvin_(HHGG).jpg')
insert_character('Character 18', 'Gospel', 'Kirk Franklin', '250px-Timothy_Lovejoy,_Jr..png')
insert_character('Character 19', 'Indie', 'Arctic Monkeys', 'Daria_Morgendorffer.png')
insert_character('Character 20', 'Grunge', 'Nirvana', 'f14e013291a31c664f5663cb2811a5aa.jpg')
insert_character('Character 21', 'Alternative', 'Radiohead', 'Adventure_Time_-_Marceline.png')
insert_character('Character 22', 'House', 'David Guetta', 'BobbyGhost.jpg')
insert_character('Character 23', 'Trance', 'Armin van Buuren', 'lunaloud.png')
insert_character('Character 24', 'Techno', 'Carl Cox', 'Gadgetputs-ezgif.com-webp-to-jpg-converter-1.jpg')
insert_character('Character 25', 'K-Pop', 'BTS', 'jem.jpg')
insert_character('Character 26', 'Reggaeton', 'J Balvin', 'http://example.com/image26.jpg')
insert_character('Character 27', 'Ska', 'The Specials', 'http://example.com/image27.jpg')
insert_character('Character 28', 'Emo', 'My Chemical Romance', 'http://example.com/image28.jpg')
insert_character('Character 29', 'Ambient', 'Brian Eno', 'http://example.com/image29.jpg')
insert_character('Character 30', 'New Age', 'Enya', 'http://example.com/image30.jpg')
