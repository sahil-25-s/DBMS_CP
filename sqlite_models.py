import sqlite3
import json
import os
from datetime import datetime

class Database:
    DB_PATH = 'movienight.db'
    
    @staticmethod
    def get_connection():
        try:
            return sqlite3.connect(Database.DB_PATH)
        except Exception as e:
            print(f"SQLite connection error: {e}")
            return None

    @staticmethod
    def init_database():
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    duration INTEGER,
                    genre TEXT,
                    language TEXT,
                    release_date DATE,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS theaters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT,
                    total_seats INTEGER DEFAULT 100,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_id INTEGER,
                    theater_id INTEGER,
                    show_date DATE,
                    show_time TIME,
                    price REAL,
                    available_seats INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (movie_id) REFERENCES movies(id),
                    FOREIGN KEY (theater_id) REFERENCES theaters(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    show_id INTEGER,
                    customer_name TEXT,
                    customer_email TEXT,
                    customer_phone TEXT,
                    seats_booked INTEGER,
                    seat_numbers TEXT,
                    total_amount REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (show_id) REFERENCES shows(id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    movie_id INTEGER,
                    customer_name TEXT,
                    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                    review_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (movie_id) REFERENCES movies(id)
                )
            """)
            
            connection.commit()
            return True
            
        except Exception as e:
            print(f"Database initialization error: {e}")
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
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies ORDER BY created_at DESC")
        movies = []
        for row in cursor.fetchall():
            movies.append({
                'id': row[0], 'title': row[1], 'description': row[2],
                'duration': row[3], 'genre': row[4], 'language': row[5],
                'release_date': row[6], 'image_url': row[7], 'created_at': row[8]
            })
        cursor.close()
        connection.close()
        return movies
    
    @staticmethod
    def get_by_id(movie_id):
        connection = Database.get_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if row:
            return {
                'id': row[0], 'title': row[1], 'description': row[2],
                'duration': row[3], 'genre': row[4], 'language': row[5],
                'release_date': row[6], 'image_url': row[7], 'created_at': row[8]
            }
        return None
    
    @staticmethod
    def create(data):
        connection = Database.get_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
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
        except Exception as e:
            print(f"Movie creation error: {e}")
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
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM theaters ORDER BY created_at DESC")
        theaters = []
        for row in cursor.fetchall():
            theaters.append({
                'id': row[0], 'name': row[1], 'location': row[2],
                'total_seats': row[3], 'created_at': row[4]
            })
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
                VALUES (?, ?, ?)
            """, (data.get('name', ''), data.get('location', ''), int(data.get('total_seats', 100))))
            connection.commit()
            return True
        except Exception as e:
            print(f"Theater creation error: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

class Show:
    @staticmethod
    def get_all():
        connection = Database.get_connection()
        if not connection:
            return []
        
        cursor = connection.cursor()
        cursor.execute("""
            SELECT s.*, m.title, t.name as theater_name
            FROM shows s
            JOIN movies m ON s.movie_id = m.id
            JOIN theaters t ON s.theater_id = t.id
            ORDER BY s.created_at DESC
        """)
        shows = []
        for row in cursor.fetchall():
            shows.append({
                'id': row[0], 'movie_id': row[1], 'theater_id': row[2],
                'show_date': row[3], 'show_time': row[4], 'price': row[5],
                'available_seats': row[6], 'created_at': row[7],
                'title': row[8], 'theater_name': row[9]
            })
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
            # Get theater total seats
            cursor.execute("SELECT total_seats FROM theaters WHERE id = ?", (data.get('theater_id'),))
            theater = cursor.fetchone()
            available_seats = theater[0] if theater else 100
            
            cursor.execute("""
                INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data.get('movie_id'), data.get('theater_id'), data.get('show_date'),
                data.get('show_time'), float(data.get('price', 0)), available_seats
            ))
            connection.commit()
            return True
        except Exception as e:
            print(f"Show creation error: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

class Booking:
    @staticmethod
    def get_all():
        return []

class Review:
    @staticmethod
    def get_by_movie_id(movie_id):
        return []