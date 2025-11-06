import mysql.connector
import os
import json
from datetime import datetime

class Database:
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', ''),
                database=os.environ.get('DB_NAME', 'moviehub'),
                port=int(os.environ.get('DB_PORT', 3306))
            )
        except mysql.connector.Error:
            return None

    @staticmethod
    def init_database():
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        try:
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    duration INT,
                    genre VARCHAR(100),
                    language VARCHAR(50),
                    release_date DATE,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS theaters (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    total_seats INT DEFAULT 100,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shows (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    movie_id INT,
                    theater_id INT,
                    show_date DATE,
                    show_time TIME,
                    price DECIMAL(10,2),
                    available_seats INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (movie_id) REFERENCES movies(id),
                    FOREIGN KEY (theater_id) REFERENCES theaters(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    show_id INT,
                    customer_name VARCHAR(255),
                    customer_email VARCHAR(255),
                    customer_phone VARCHAR(20),
                    seats_booked INT,
                    seat_numbers JSON,
                    total_amount DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (show_id) REFERENCES shows(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    movie_id INT,
                    customer_name VARCHAR(255),
                    rating INT CHECK (rating >= 1 AND rating <= 5),
                    review_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (movie_id) REFERENCES movies(id)
                )
            """)
            
            connection.commit()
            return True
            
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            connection.close()

class Movie:
    @staticmethod
    def get_all():
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies ORDER BY created_at DESC")
        movies = cursor.fetchall()
        cursor.close()
        connection.close()
        return movies
    
    @staticmethod
    def get_by_id(movie_id):
        connection = Database.get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()
        cursor.close()
        connection.close()
        return movie
    
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data.get('title', ''),
                data.get('description', ''),
                int(data.get('duration', 0)) if data.get('duration') else 0,
                data.get('genre', ''),
                data.get('language', ''),
                data.get('release_date') if data.get('release_date') else None,
                data.get('image_url', '')
            ))
            connection.commit()
            return True
        except Exception:
            return False
        finally:
            cursor.close()
            connection.close()

class Theater:
    @staticmethod
    def get_all():
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM theaters ORDER BY created_at DESC")
        theaters = cursor.fetchall()
        cursor.close()
        connection.close()
        return theaters
    
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO theaters (name, location, total_seats)
                VALUES (%s, %s, %s)
            """, (data['name'], data['location'], int(data['total_seats'])))
            connection.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            connection.close()

class Show:
    @staticmethod
    def get_by_movie_id(movie_id):
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, t.name as theater_name, t.location
            FROM shows s
            JOIN theaters t ON s.theater_id = t.id
            WHERE s.movie_id = %s AND s.show_date >= CURDATE()
            ORDER BY s.show_date, s.show_time
        """, (movie_id,))
        shows = cursor.fetchall()
        cursor.close()
        connection.close()
        return shows
    
    @staticmethod
    def get_by_id(show_id):
        connection = Database.get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.title, t.name as theater_name, t.location, t.total_seats
            FROM shows s
            JOIN movies m ON s.movie_id = m.id
            JOIN theaters t ON s.theater_id = t.id
            WHERE s.id = %s
        """, (show_id,))
        show = cursor.fetchone()
        cursor.close()
        connection.close()
        return show
    
    @staticmethod
    def get_all():
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, m.title, t.name as theater_name
            FROM shows s
            JOIN movies m ON s.movie_id = m.id
            JOIN theaters t ON s.theater_id = t.id
            ORDER BY s.created_at DESC
        """)
        shows = cursor.fetchall()
        cursor.close()
        connection.close()
        return shows
    
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT total_seats FROM theaters WHERE id = %s", (data['theater_id'],))
            theater = cursor.fetchone()
            
            cursor.execute("""
                INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data['movie_id'], data['theater_id'], data['show_date'],
                data['show_time'], float(data['price']), theater[0] if theater else 100
            ))
            connection.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            connection.close()

class Booking:
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO bookings (show_id, customer_name, customer_email, customer_phone,
                                    seats_booked, seat_numbers, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data['show_id'], data['customer_name'], data['customer_email'],
                data['customer_phone'], len(data['selected_seats']),
                json.dumps(data['selected_seats']), data['total_amount']
            ))
            
            cursor.execute("""
                UPDATE shows SET available_seats = available_seats - %s WHERE id = %s
            """, (len(data['selected_seats']), data['show_id']))
            
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error:
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def get_by_id(booking_id):
        connection = Database.get_connection()
        if not connection:
            return None
        
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
        return booking
    
    @staticmethod
    def get_all():
        connection = Database.get_connection()
        if not connection:
            return []
        
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
        return bookings

class Review:
    @staticmethod
    def get_by_movie_id(movie_id):
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM reviews WHERE movie_id = %s ORDER BY created_at DESC
        """, (movie_id,))
        reviews = cursor.fetchall()
        cursor.close()
        connection.close()
        return reviews
    
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO reviews (movie_id, customer_name, rating, review_text)
                VALUES (%s, %s, %s, %s)
            """, (data['movie_id'], data['customer_name'], data['rating'], data['review_text']))
            connection.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            connection.close()