from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
from datetime import datetime, timedelta
import json
import secrets
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'static/images/movies'

# Database configuration
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'database': os.environ.get('DB_NAME', 'movie_booking_system'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'autocommit': True
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def init_database():
    """Initialize database and create tables if they don't exist"""
    connection = get_db_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_booking_system")
        cursor.execute("USE movie_booking_system")
        
        # Movies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                duration INT NOT NULL,
                genre VARCHAR(100),
                language VARCHAR(50),
                release_date DATE,
                image_url VARCHAR(255),
                rating DECIMAL(3,1) DEFAULT 0,
                total_reviews INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Theaters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS theaters (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                total_seats INT NOT NULL DEFAULT 100,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Shows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                theater_id INT,
                show_date DATE NOT NULL,
                show_time TIME NOT NULL,
                price DECIMAL(8,2) NOT NULL,
                available_seats INT DEFAULT 100,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
                FOREIGN KEY (theater_id) REFERENCES theaters(id) ON DELETE CASCADE
            )
        """)
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                show_id INT,
                customer_name VARCHAR(255) NOT NULL,
                customer_email VARCHAR(255) NOT NULL,
                customer_phone VARCHAR(20) NOT NULL,
                seats_booked INT NOT NULL,
                seat_numbers TEXT,
                total_amount DECIMAL(10,2) NOT NULL,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'confirmed',
                FOREIGN KEY (show_id) REFERENCES shows(id) ON DELETE CASCADE
            )
        """)
        
        # Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                customer_name VARCHAR(255) NOT NULL,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                review_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("Database initialized successfully!")
        return True
        
    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

# Routes
@app.route('/')
def home():
    connection = get_db_connection()
    if not connection:
        # Fallback with sample data when database is not available
        sample_movies = [
            {
                'id': 1,
                'title': 'Sample Movie',
                'description': 'Database not connected. Please configure environment variables.',
                'genre': 'Demo',
                'duration': 120,
                'language': 'English',
                'avg_rating': 4.5,
                'review_count': 0,
                'image_url': 'https://via.placeholder.com/300x400?text=No+Database'
            }
        ]
        return render_template('home.html', movies=sample_movies)
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get all movies with their ratings
        cursor.execute("""
            SELECT m.*, COALESCE(AVG(r.rating), 0) as avg_rating, COUNT(r.id) as review_count
            FROM movies m
            LEFT JOIN reviews r ON m.id = r.movie_id
            GROUP BY m.id
            ORDER BY m.created_at DESC
        """)
        movies = cursor.fetchall()
    except:
        movies = []
    
    cursor.close()
    connection.close()
    
    return render_template('home.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    
    # Get movie details
    cursor.execute("""
        SELECT m.*, COALESCE(AVG(r.rating), 0) as avg_rating, COUNT(r.id) as review_count
        FROM movies m
        LEFT JOIN reviews r ON m.id = r.movie_id
        WHERE m.id = %s
        GROUP BY m.id
    """, (movie_id,))
    movie = cursor.fetchone()
    
    if not movie:
        return render_template('error.html', message="Movie not found")
    
    # Get available shows
    cursor.execute("""
        SELECT s.*, t.name as theater_name, t.location
        FROM shows s
        JOIN theaters t ON s.theater_id = t.id
        WHERE s.movie_id = %s AND s.show_date >= CURDATE()
        ORDER BY s.show_date, s.show_time
    """, (movie_id,))
    shows = cursor.fetchall()
    
    # Get reviews
    cursor.execute("""
        SELECT * FROM reviews
        WHERE movie_id = %s
        ORDER BY created_at DESC
        LIMIT 10
    """, (movie_id,))
    reviews = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('movie_details.html', movie=movie, shows=shows, reviews=reviews)

@app.route('/book/<int:show_id>')
def book_seats(show_id):
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    
    # Get show details
    cursor.execute("""
        SELECT s.*, m.title, m.duration, t.name as theater_name, t.location, t.total_seats
        FROM shows s
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        WHERE s.id = %s
    """, (show_id,))
    show = cursor.fetchone()
    
    if not show:
        return render_template('error.html', message="Show not found")
    
    # Get booked seats
    cursor.execute("""
        SELECT seat_numbers FROM bookings
        WHERE show_id = %s AND status = 'confirmed'
    """, (show_id,))
    bookings = cursor.fetchall()
    
    booked_seats = []
    for booking in bookings:
        if booking['seat_numbers']:
            seats = json.loads(booking['seat_numbers'])
            booked_seats.extend(seats)
    
    cursor.close()
    connection.close()
    
    return render_template('book_seats.html', show=show, booked_seats=booked_seats)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    cursor = connection.cursor()
    
    try:
        # Insert booking
        cursor.execute("""
            INSERT INTO bookings (show_id, customer_name, customer_email, customer_phone,
                                seats_booked, seat_numbers, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['show_id'],
            data['customer_name'],
            data['customer_email'],
            data['customer_phone'],
            len(data['selected_seats']),
            json.dumps(data['selected_seats']),
            data['total_amount']
        ))
        
        # Update available seats
        cursor.execute("""
            UPDATE shows SET available_seats = available_seats - %s
            WHERE id = %s
        """, (len(data['selected_seats']), data['show_id']))
        
        connection.commit()
        booking_id = cursor.lastrowid
        
        return jsonify({'success': True, 'booking_id': booking_id})
    
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'success': False, 'message': str(err)})
    
    finally:
        cursor.close()
        connection.close()

@app.route('/booking_success/<int:booking_id>')
def booking_success(booking_id):
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT b.*, s.show_date, s.show_time, s.price,
               m.title, t.name as theater_name, t.location
        FROM bookings b
        JOIN shows s ON b.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        WHERE b.id = %s
    """, (booking_id,))
    booking = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not booking:
        return render_template('error.html', message="Booking not found")
    
    return render_template('booking_success.html', booking=booking)

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO reviews (movie_id, customer_name, rating, review_text)
            VALUES (%s, %s, %s, %s)
        """, (
            data['movie_id'],
            data['customer_name'],
            data['rating'],
            data['review_text']
        ))
        
        connection.commit()
        return jsonify({'success': True})
    
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)})
    
    finally:
        cursor.close()
        connection.close()

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', datetime=datetime)

@app.route('/admin/movies')
def admin_movies():
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies ORDER BY created_at DESC")
    movies = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('admin/movies.html', movies=movies)

@app.route('/admin/theaters')
def admin_theaters():
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM theaters ORDER BY created_at DESC")
    theaters = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('admin/theaters.html', theaters=theaters)

@app.route('/admin/shows')
def admin_shows():
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, m.title, t.name as theater_name
        FROM shows s
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        ORDER BY s.created_at DESC
    """)
    shows = cursor.fetchall()
    
    cursor.execute("SELECT * FROM movies ORDER BY title")
    movies = cursor.fetchall()
    
    cursor.execute("SELECT * FROM theaters ORDER BY name")
    theaters = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('admin/shows.html', shows=shows, movies=movies, theaters=theaters)

@app.route('/admin/add_movie', methods=['POST'])
def add_movie():
    data = request.form
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection error'})
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['title'],
            data['description'],
            int(data['duration']),
            data['genre'],
            data['language'],
            data['release_date'],
            data['image_url']
        ))
        
        connection.commit()
        flash('Movie added successfully!', 'success')
    
    except mysql.connector.Error as err:
        flash(f'Error: {str(err)}', 'error')
    
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('admin_movies'))

@app.route('/admin/add_theater', methods=['POST'])
def add_theater():
    data = request.form
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error', 'error')
        return redirect(url_for('admin_theaters'))
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO theaters (name, location, total_seats)
            VALUES (%s, %s, %s)
        """, (
            data['name'],
            data['location'],
            int(data['total_seats'])
        ))
        
        connection.commit()
        flash('Theater added successfully!', 'success')
    
    except mysql.connector.Error as err:
        flash(f'Error: {str(err)}', 'error')
    
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('admin_theaters'))

@app.route('/admin/add_show', methods=['POST'])
def add_show():
    data = request.form
    
    connection = get_db_connection()
    if not connection:
        flash('Database connection error', 'error')
        return redirect(url_for('admin_shows'))
    
    cursor = connection.cursor()
    
    try:
        # Get theater's total seats
        cursor.execute("SELECT total_seats FROM theaters WHERE id = %s", (data['theater_id'],))
        theater = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['movie_id'],
            data['theater_id'],
            data['show_date'],
            data['show_time'],
            float(data['price']),
            theater[0] if theater else 100
        ))
        
        connection.commit()
        flash('Show added successfully!', 'success')
    
    except mysql.connector.Error as err:
        flash(f'Error: {str(err)}', 'error')
    
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('admin_shows'))

@app.route('/admin/bookings')
def admin_bookings():
    connection = get_db_connection()
    if not connection:
        return render_template('error.html', message="Database connection error")
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.*, s.show_date, s.show_time,
               m.title, t.name as theater_name
        FROM bookings b
        JOIN shows s ON b.show_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theaters t ON s.theater_id = t.id
        ORDER BY b.created_at DESC
    """)
    bookings = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/init-db')
def init_db_route():
    """Initialize database remotely for cloud deployment"""
    if init_database():
        return jsonify({'success': True, 'message': 'Database initialized successfully'})
    else:
        return jsonify({'success': False, 'message': 'Database initialization failed'})

if __name__ == '__main__':
    # Initialize database on startup for local development
    if os.environ.get('DB_HOST') == 'localhost':
        init_database()
    app.run(debug=True, port=5000)