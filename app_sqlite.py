from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    conn = sqlite3.connect('moviehub.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration INTEGER NOT NULL,
            genre TEXT,
            language TEXT,
            release_date DATE,
            image_url TEXT,
            rating REAL DEFAULT 0,
            total_reviews INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS theaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            total_seats INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            theater_id INTEGER,
            show_date DATE NOT NULL,
            show_time TIME NOT NULL,
            price REAL NOT NULL,
            available_seats INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (movie_id) REFERENCES movies (id),
            FOREIGN KEY (theater_id) REFERENCES theaters (id)
        )
    ''')
    
    # Insert sample data
    sample_movies = [
        ('Avengers: Endgame', 'Epic superhero finale', 181, 'Action', 'English', '2019-04-26', 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg'),
        ('Spider-Man: No Way Home', 'Multiverse adventure', 148, 'Action', 'English', '2021-12-17', 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg')
    ]
    
    for movie in sample_movies:
        conn.execute('INSERT OR IGNORE INTO movies (title, description, duration, genre, language, release_date, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)', movie)
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('home.html', movies=movies)

@app.route('/init-db')
def init_db_route():
    init_database()
    return jsonify({'success': True, 'message': 'Database initialized'})

if __name__ == '__main__':
    init_database()
    app.run(debug=True)