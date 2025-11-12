import sqlite3

def get_db():
    conn = sqlite3.connect(':memory:')  # In-memory database
    conn.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        duration INTEGER,
        genre TEXT,
        language TEXT,
        release_date TEXT,
        image_url TEXT
    )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS theaters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        total_seats INTEGER DEFAULT 100
    )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS shows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        theater_id INTEGER,
        show_date TEXT,
        show_time TEXT,
        price REAL,
        available_seats INTEGER
    )''')
    
    return conn

# Global database connection
db_conn = get_db()

def add_movie(title, description, duration, genre, language, release_date, image_url):
    cursor = db_conn.cursor()
    cursor.execute('''INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (title, description, duration, genre, language, release_date, image_url))
    db_conn.commit()
    return cursor.lastrowid

def get_all_movies():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM movies')
    return cursor.fetchall()

def add_theater(name, location, total_seats):
    cursor = db_conn.cursor()
    cursor.execute('''INSERT INTO theaters (name, location, total_seats)
                     VALUES (?, ?, ?)''', (name, location, total_seats))
    db_conn.commit()
    return cursor.lastrowid

def get_all_theaters():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM theaters')
    return cursor.fetchall()

def add_show(movie_id, theater_id, show_date, show_time, price, available_seats):
    cursor = db_conn.cursor()
    cursor.execute('''INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                   (movie_id, theater_id, show_date, show_time, price, available_seats))
    db_conn.commit()
    return cursor.lastrowid

def get_all_shows():
    cursor = db_conn.cursor()
    cursor.execute('''SELECT s.*, m.title, t.name as theater_name 
                     FROM shows s 
                     LEFT JOIN movies m ON s.movie_id = m.id 
                     LEFT JOIN theaters t ON s.theater_id = t.id''')
    return cursor.fetchall()