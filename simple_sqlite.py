import sqlite3
import os

# Use a simple file-based SQLite database
DB_PATH = '/tmp/movienight.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        duration INTEGER,
        genre TEXT,
        language TEXT,
        release_date TEXT,
        image_url TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS theaters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        total_seats INTEGER DEFAULT 100
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        theater_id INTEGER,
        show_date TEXT,
        show_time TEXT,
        price REAL,
        available_seats INTEGER
    )''')
    
    conn.commit()
    conn.close()

def add_movie(title, description, duration, genre, language, release_date, image_url):
    conn = get_connection()
    cursor = conn.cursor()
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