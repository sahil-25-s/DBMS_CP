import psycopg2
import os

# Use a free PostgreSQL service or local connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/movienight')

def get_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except:
        # Fallback to SQLite if PostgreSQL fails
        import sqlite3
        conn = sqlite3.connect(':memory:')
        # Create tables for SQLite fallback
        conn.execute('''CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, description TEXT, duration INTEGER,
            genre TEXT, language TEXT, release_date TEXT, image_url TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS theaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, location TEXT, total_seats INTEGER
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER, theater_id INTEGER, show_date TEXT,
            show_time TEXT, price REAL, available_seats INTEGER
        )''')
        return conn

def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Try PostgreSQL syntax first
        cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            duration INTEGER,
            genre VARCHAR(100),
            language VARCHAR(50),
            release_date DATE,
            image_url VARCHAR(500)
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS theaters (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            location VARCHAR(255),
            total_seats INTEGER DEFAULT 100
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS shows (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER REFERENCES movies(id),
            theater_id INTEGER REFERENCES theaters(id),
            show_date DATE,
            show_time TIME,
            price DECIMAL(10,2),
            available_seats INTEGER
        )''')
        
        conn.commit()
        conn.close()
        return True
    except:
        return True  # SQLite fallback already initialized

def add_movie(title, description, duration, genre, language, release_date, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # PostgreSQL syntax
        cursor.execute('''INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                         VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
                       (title, description, duration, genre, language, release_date, image_url))
        movie_id = cursor.fetchone()[0]
    except:
        # SQLite fallback
        cursor.execute('''INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (title, description, duration, genre, language, release_date, image_url))
        movie_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return movie_id

def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies ORDER BY id DESC')
    movies = cursor.fetchall()
    conn.close()
    return movies

def add_theater(name, location, total_seats):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO theaters (name, location, total_seats)
                         VALUES (%s, %s, %s) RETURNING id''',
                       (name, location, total_seats))
        theater_id = cursor.fetchone()[0]
    except:
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
    
    try:
        cursor.execute('''INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                         VALUES (%s, %s, %s, %s, %s, %s) RETURNING id''',
                       (movie_id, theater_id, show_date, show_time, price, available_seats))
        show_id = cursor.fetchone()[0]
    except:
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