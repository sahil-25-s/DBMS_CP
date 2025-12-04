import sqlite3
import os

# Use a simple file-based SQLite database in current directory
DB_PATH = 'movienight.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Creating database tables with SQL...")
    
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
    print("Movies table created")
    
    # Create theaters table
    theaters_sql = '''CREATE TABLE IF NOT EXISTS theaters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        total_seats INTEGER DEFAULT 100
    )'''
    cursor.execute(theaters_sql)
    print("Theaters table created")
    
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
    print("Shows table created")
    
    # Add sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM movies')
    if cursor.fetchone()[0] == 0:
        print("Adding sample movies...")
        sample_movies = [
            ('Avengers: Endgame', 'Epic superhero finale', 181, 'Action', 'English', '2024-01-15', 'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg'),
            ('Spider-Man', 'Friendly neighborhood hero', 148, 'Action', 'English', '2024-02-01', 'https://upload.wikimedia.org/wikipedia/en/2/21/Web_of_Spider-Man_Vol_1_129-1.png'),
            ('The Dark Knight', 'Batman vs Joker', 152, 'Action', 'English', '2024-01-20', 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg')
        ]
        
        for movie in sample_movies:
            cursor.execute('INSERT INTO movies (title, description, duration, genre, language, release_date, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)', movie)
        print(f"Added {len(sample_movies)} sample movies")
    else:
        # Update existing movies with proper images
        update_all_movie_images()
    
    # Add sample theaters
    cursor.execute('SELECT COUNT(*) FROM theaters')
    if cursor.fetchone()[0] == 0:
        print("Adding sample theaters...")
        sample_theaters = [
            ('PVR Cinemas', 'Mall Road', 96),
            ('INOX Theater', 'City Center', 120),
            ('Cineplex', 'Downtown', 80)
        ]
        
        for theater in sample_theaters:
            cursor.execute('INSERT INTO theaters (name, location, total_seats) VALUES (?, ?, ?)', theater)
        print(f"Added {len(sample_theaters)} sample theaters")
    
    # Add sample shows
    cursor.execute('SELECT COUNT(*) FROM shows')
    if cursor.fetchone()[0] == 0:
        print("Adding sample shows...")
        sample_shows = [
            (1, 1, '2024-12-25', '18:00', 250.0, 96),
            (1, 2, '2024-12-25', '21:00', 300.0, 120),
            (2, 1, '2024-12-26', '15:00', 200.0, 96),
            (2, 3, '2024-12-26', '19:30', 220.0, 80),
            (3, 2, '2024-12-27', '16:00', 280.0, 120),
            (3, 3, '2024-12-27', '20:00', 260.0, 80)
        ]
        
        for show in sample_shows:
            cursor.execute('INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats) VALUES (?, ?, ?, ?, ?, ?)', show)
        print(f"Added {len(sample_shows)} sample shows")
    
    # Initialize food tables
    init_food_table()
    
    conn.commit()
    conn.close()
    print("Database initialization complete!\n")

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
    
    sql_query = '''INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                   VALUES (?, ?, ?, ?, ?, ?)'''
    
    print(f"\n💾 SQL Query: {sql_query}")
    print(f"📊 Data: {(movie_id, theater_id, show_date, show_time, price, available_seats)}")
    
    cursor.execute(sql_query, (movie_id, theater_id, show_date, show_time, price, available_seats))
    show_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Show added successfully with ID: {show_id}\n")
    return show_id

def get_all_shows():
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_query = '''SELECT s.*, m.title, t.name as theater_name 
                   FROM shows s 
                   LEFT JOIN movies m ON s.movie_id = m.id 
                   LEFT JOIN theaters t ON s.theater_id = t.id
                   ORDER BY s.id DESC'''
    
    print(f"💾 SQL Query: {sql_query}")
    
    cursor.execute(sql_query)
    shows = cursor.fetchall()
    conn.close()
    
    print(f"📈 Retrieved {len(shows)} shows from database")
    return shows

def update_movie_image(movie_id, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_query = 'UPDATE movies SET image_url = ? WHERE id = ?'
    print(f"💾 SQL Query: {sql_query}")
    print(f"📊 Data: {(image_url, movie_id)}")
    
    cursor.execute(sql_query, (image_url, movie_id))
    conn.commit()
    conn.close()
    
    print(f"✅ Movie {movie_id} image updated successfully\n")

def update_all_movie_images():
    # High-quality movie poster URLs
    movie_images = {
        'Avengers: Endgame': 'https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg',
        'Spider-Man': 'https://upload.wikimedia.org/wikipedia/en/2/21/Web_of_Spider-Man_Vol_1_129-1.png',
        'The Dark Knight': 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg'
    }
    
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Updating movie poster images...")
    
    for title, image_url in movie_images.items():
        cursor.execute('SELECT id FROM movies WHERE title = ?', (title,))
        result = cursor.fetchone()
        if result:
            movie_id = result[0]
            cursor.execute('UPDATE movies SET image_url = ? WHERE id = ?', (image_url, movie_id))
            print(f"Updated {title} poster")
    
    conn.commit()
    conn.close()
    print("All movie posters updated!\n")
def get_show_by_id(show_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_query = '''SELECT s.id, s.movie_id, s.theater_id, s.show_date, s.show_time, s.price, s.available_seats, m.title, t.name as theater_name
                   FROM shows s 
                   LEFT JOIN movies m ON s.movie_id = m.id 
                   LEFT JOIN theaters t ON s.theater_id = t.id
                   WHERE s.id = ?'''
    
    cursor.execute(sql_query, (show_id,))
    show = cursor.fetchone()
    conn.close()
    
    return show

def add_booking(show_id, customer_name, customer_email, customer_phone, selected_seats, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    
    import json
    
    sql_query = '''INSERT INTO bookings (show_id, customer_name, customer_email, customer_phone, seat_numbers, total_amount)
                   VALUES (?, ?, ?, ?, ?, ?)'''
    
    cursor.execute(sql_query, (show_id, customer_name, customer_email, customer_phone, 
                              json.dumps(selected_seats), total_amount))
    
    booking_id = cursor.lastrowid
    
    # Update available seats
    cursor.execute('UPDATE shows SET available_seats = available_seats - ? WHERE id = ?', 
                  (len(selected_seats), show_id))
    
    conn.commit()
    conn.close()
    
    return booking_id

def get_booked_seats(show_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT seat_numbers FROM bookings WHERE show_id = ?', (show_id,))
    bookings = cursor.fetchall()
    conn.close()
    
    import json
    booked_seats = []
    for booking in bookings:
        if booking[0]:
            seats = json.loads(booking[0])
            booked_seats.extend(seats)
    
    return booked_seats

def get_booking_by_id(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_query = '''SELECT b.id, b.show_id, b.customer_name, b.customer_email, b.customer_phone, b.seat_numbers, b.total_amount, s.show_date, s.show_time, m.title, t.name as theater_name
                   FROM bookings b
                   LEFT JOIN shows s ON b.show_id = s.id
                   LEFT JOIN movies m ON s.movie_id = m.id
                   LEFT JOIN theaters t ON s.theater_id = t.id
                   WHERE b.id = ?'''
    
    cursor.execute(sql_query, (booking_id,))
    booking = cursor.fetchone()
    conn.close()
    
    return booking
def init_food_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS food_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER,
        items TEXT,
        total_amount REAL,
        discount_applied REAL DEFAULT 0
    )''')
    
    # Add sample food items
    cursor.execute('SELECT COUNT(*) FROM food_items')
    if cursor.fetchone()[0] == 0:
        food_items = [
            ('Popcorn (Small)', 150, 'Snacks'),
            ('Popcorn (Large)', 250, 'Snacks'),
            ('Nachos', 200, 'Snacks'),
            ('Hot Dog', 180, 'Snacks'),
            ('Coke (Small)', 80, 'Drinks'),
            ('Coke (Large)', 120, 'Drinks'),
            ('Water Bottle', 50, 'Drinks'),
            ('Combo 1 (Popcorn + Coke)', 200, 'Combos'),
            ('Combo 2 (Nachos + Coke)', 250, 'Combos')
        ]
        
        for item in food_items:
            cursor.execute('INSERT INTO food_items (name, price, category) VALUES (?, ?, ?)', item)
    
    conn.commit()
    conn.close()

def get_food_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM food_items ORDER BY category, name')
    items = cursor.fetchall()
    conn.close()
    return items

def add_food_order(booking_id, items, total_amount, discount_applied=0):
    conn = get_connection()
    cursor = conn.cursor()
    
    import json
    cursor.execute('INSERT INTO food_orders (booking_id, items, total_amount, discount_applied) VALUES (?, ?, ?, ?)',
                  (booking_id, json.dumps(items), total_amount, discount_applied))
    
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id
def delete_movie(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0