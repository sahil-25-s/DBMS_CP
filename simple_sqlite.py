import sqlite3
import os

# Use a simple file-based SQLite database in current directory
DB_PATH = 'movienight.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("💾 Creating database tables with SQL...")
    
    # Create movies table
    movies_sql = '''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        duration INTEGER,
        genre TEXT,
        language TEXT,
        release_date TEXT,
        image_url TEXT
    )'''
    cursor.execute(movies_sql)
    print("✅ Movies table created")
    
    # Create theaters table
    theaters_sql = '''CREATE TABLE IF NOT EXISTS theaters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        total_seats INTEGER DEFAULT 100
    )'''
    cursor.execute(theaters_sql)
    print("✅ Theaters table created")
    
    # Create shows table
    shows_sql = '''CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        theater_id INTEGER,
        show_date TEXT,
        show_time TEXT,
        price REAL,
        available_seats INTEGER
    )'''
    cursor.execute(shows_sql)
    print("✅ Shows table created")
    
    # Add sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM movies')
    if cursor.fetchone()[0] == 0:
        print("🎬 Adding sample movies...")
        sample_movies = [
            ('Avengers: Endgame', 'Epic superhero finale', 181, 'Action', 'English', '2024-01-15', 'https://via.placeholder.com/300x450'),
            ('Spider-Man', 'Friendly neighborhood hero', 148, 'Action', 'English', '2024-02-01', 'https://via.placeholder.com/300x450'),
            ('The Dark Knight', 'Batman vs Joker', 152, 'Action', 'English', '2024-01-20', 'https://via.placeholder.com/300x450')
        ]
        
        for movie in sample_movies:
            cursor.execute('INSERT INTO movies (title, description, duration, genre, language, release_date, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)', movie)
        print(f"✅ Added {len(sample_movies)} sample movies")
    
    conn.commit()
    conn.close()
    print("💾 Database initialization complete!\n")

def add_movie(title, description, duration, genre, language, release_date, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    
    # SQL INSERT operation
    sql_query = '''INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
    
    print(f"\n💾 SQL Query: {sql_query}")
    print(f"📊 Data: {(title, description, duration, genre, language, release_date, image_url)}")
    
    cursor.execute(sql_query, (title, description, duration, genre, language, release_date, image_url))
    movie_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Movie added successfully with ID: {movie_id}\n")
    return movie_id

def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    
    # SQL SELECT operation
    sql_query = 'SELECT * FROM movies ORDER BY id DESC'
    print(f"💾 SQL Query: {sql_query}")
    
    cursor.execute(sql_query)
    movies = cursor.fetchall()
    conn.close()
    
    print(f"📈 Retrieved {len(movies)} movies from database")
    return movies

def add_theater(name, location, total_seats):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO theaters (name, location, total_seats)
                     VALUES (?, ?, ?)''', (name, location, total_seats))
    theater_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return theater_id

def get_all_theaters():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM theaters')
    theaters = cursor.fetchall()
    conn.close()
    return theaters

def add_show(movie_id, theater_id, show_date, show_time, price, available_seats):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                   (movie_id, theater_id, show_date, show_time, price, available_seats))
    show_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return show_id

def get_all_shows():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT s.*, m.title, t.name as theater_name 
                     FROM shows s 
                     LEFT JOIN movies m ON s.movie_id = m.id 
                     LEFT JOIN theaters t ON s.theater_id = t.id''')
    shows = cursor.fetchall()
    conn.close()
    return shows