#!/usr/bin/env python3
"""
Database Initialization Script for MovieHub
This script creates the database and populates it with sample data.
"""

import mysql.connector
from datetime import datetime, timedelta
import json
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Update with your MySQL password
    'database': 'movie_booking_system'
}

def get_connection(create_db=False):
    """Get database connection"""
    config = DB_CONFIG.copy()
    if create_db:
        config.pop('database')
    
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def create_database():
    """Create the database if it doesn't exist"""
    connection = get_connection(create_db=True)
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_booking_system")
        print("✓ Database created successfully")
        return True
    except mysql.connector.Error as err:
        print(f"✗ Error creating database: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

def create_tables():
    """Create all required tables"""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    tables = {
        'movies': """
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
        """,
        
        'theaters': """
            CREATE TABLE IF NOT EXISTS theaters (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                total_seats INT NOT NULL DEFAULT 100,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        
        'shows': """
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
        """,
        
        'bookings': """
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
        """,
        
        'reviews': """
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                customer_name VARCHAR(255) NOT NULL,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                review_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
            )
        """
    }
    
    try:
        for table_name, table_sql in tables.items():
            cursor.execute(table_sql)
            print(f"✓ Table '{table_name}' created successfully")
        
        connection.commit()
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Error creating tables: {err}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def insert_sample_movies():
    """Insert sample movies"""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    sample_movies = [
        {
            'title': 'Avengers: Endgame',
            'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos\' actions and restore order to the universe.',
            'duration': 181,
            'genre': 'Action',
            'language': 'English',
            'release_date': '2019-04-26',
            'image_url': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg'
        },
        {
            'title': 'Spider-Man: No Way Home',
            'description': 'Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero. When he asks for help from Doctor Strange the stakes become even more dangerous, forcing him to discover what it truly means to be Spider-Man.',
            'duration': 148,
            'genre': 'Action',
            'language': 'English',
            'release_date': '2021-12-17',
            'image_url': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg'
        },
        {
            'title': 'The Dark Knight',
            'description': 'Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets.',
            'duration': 152,
            'genre': 'Action',
            'language': 'English',
            'release_date': '2008-07-18',
            'image_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
        },
        {
            'title': 'Inception',
            'description': 'Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, stealing valuable secrets from deep within the subconscious during the dream state, when the mind is at its most vulnerable.',
            'duration': 148,
            'genre': 'Sci-Fi',
            'language': 'English',
            'release_date': '2010-07-16',
            'image_url': 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg'
        },
        {
            'title': 'Dangal',
            'description': 'Mahavir Singh Phogat, a former wrestler, decides to fulfill his dream of winning a gold medal for his country by training his daughters for the Commonwealth Games despite the existing social stigmas.',
            'duration': 161,
            'genre': 'Drama',
            'language': 'Hindi',
            'release_date': '2016-12-23',
            'image_url': 'https://image.tmdb.org/t/p/w500/lzYjv4wAtzgvDbRNwkHi9g9tLLW.jpg'
        },
        {
            'title': '3 Idiots',
            'description': 'Rascal. Joker. Dreamer. Genius... You\'ve never met a college student quite like "Rancho." From the moment he arrives at India\'s most prestigious university, Rancho\'s outlandish schemes turn the campus upside down—along with the lives of his two newfound best friends.',
            'duration': 170,
            'genre': 'Comedy',
            'language': 'Hindi',
            'release_date': '2009-12-25',
            'image_url': 'https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssoloscw1MQYfCu.jpg'
        }
    ]
    
    try:
        insert_query = """
            INSERT INTO movies (title, description, duration, genre, language, release_date, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for movie in sample_movies:
            cursor.execute(insert_query, (
                movie['title'],
                movie['description'],
                movie['duration'],
                movie['genre'],
                movie['language'],
                movie['release_date'],
                movie['image_url']
            ))
        
        connection.commit()
        print(f"✓ {len(sample_movies)} sample movies inserted successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Error inserting movies: {err}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def insert_sample_theaters():
    """Insert sample theaters"""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    sample_theaters = [
        {
            'name': 'PVR Cinemas',
            'location': 'Phoenix Mall, Kurla West, Mumbai - 400070',
            'total_seats': 120
        },
        {
            'name': 'INOX Multiplex',
            'location': 'R City Mall, Ghatkopar West, Mumbai - 400086',
            'total_seats': 150
        },
        {
            'name': 'Cinepolis',
            'location': 'Viviana Mall, Thane West, Thane - 400601',
            'total_seats': 100
        },
        {
            'name': 'BookMyShow Drive-In',
            'location': 'Jio World Drive, BKC, Mumbai - 400051',
            'total_seats': 80
        }
    ]
    
    try:
        insert_query = """
            INSERT INTO theaters (name, location, total_seats)
            VALUES (%s, %s, %s)
        """
        
        for theater in sample_theaters:
            cursor.execute(insert_query, (
                theater['name'],
                theater['location'],
                theater['total_seats']
            ))
        
        connection.commit()
        print(f"✓ {len(sample_theaters)} sample theaters inserted successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Error inserting theaters: {err}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def insert_sample_shows():
    """Insert sample shows for the next 7 days"""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Get movie and theater IDs
        cursor.execute("SELECT id FROM movies")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id, total_seats FROM theaters")
        theater_data = cursor.fetchall()
        
        if not movie_ids or not theater_data:
            print("✗ No movies or theaters found. Please add them first.")
            return False
        
        show_times = ['09:00:00', '12:30:00', '16:00:00', '19:30:00', '22:00:00']
        base_prices = [150, 200, 250, 300, 180, 220]
        
        insert_query = """
            INSERT INTO shows (movie_id, theater_id, show_date, show_time, price, available_seats)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        shows_count = 0
        
        # Create shows for the next 7 days
        for day_offset in range(7):
            show_date = (datetime.now() + timedelta(days=day_offset)).date()
            
            for movie_id in movie_ids[:4]:  # Use first 4 movies
                for theater_id, total_seats in theater_data[:2]:  # Use first 2 theaters
                    for time_slot in show_times[:3]:  # Use first 3 time slots
                        price = base_prices[movie_id % len(base_prices)]
                        
                        cursor.execute(insert_query, (
                            movie_id,
                            theater_id,
                            show_date,
                            time_slot,
                            price,
                            total_seats
                        ))
                        shows_count += 1
        
        connection.commit()
        print(f"✓ {shows_count} sample shows inserted successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Error inserting shows: {err}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def insert_sample_reviews():
    """Insert sample reviews"""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Get movie IDs
        cursor.execute("SELECT id FROM movies")
        movie_ids = [row[0] for row in cursor.fetchall()]
        
        if not movie_ids:
            print("✗ No movies found. Please add them first.")
            return False
        
        sample_reviews = [
            {
                'customer_name': 'Rajesh Kumar',
                'rating': 5,
                'review_text': 'Absolutely amazing movie! Great storyline and excellent acting. Highly recommended!'
            },
            {
                'customer_name': 'Priya Sharma',
                'rating': 4,
                'review_text': 'Really enjoyed watching this. Good direction and cinematography. Worth the money!'
            },
            {
                'customer_name': 'Amit Singh',
                'rating': 5,
                'review_text': 'One of the best movies I have watched this year. Phenomenal performances!'
            },
            {
                'customer_name': 'Sneha Patel',
                'rating': 4,
                'review_text': 'Great movie experience. The theater was comfortable and the movie was engaging.'
            },
            {
                'customer_name': 'Rohit Mehta',
                'rating': 3,
                'review_text': 'Decent movie but could have been better. Average storyline but good acting.'
            }
        ]
        
        insert_query = """
            INSERT INTO reviews (movie_id, customer_name, rating, review_text)
            VALUES (%s, %s, %s, %s)
        """
        
        reviews_count = 0
        
        # Add 2-3 reviews for each movie
        for movie_id in movie_ids:
            for i in range(2):  # 2 reviews per movie
                review = sample_reviews[reviews_count % len(sample_reviews)]
                cursor.execute(insert_query, (
                    movie_id,
                    review['customer_name'],
                    review['rating'],
                    review['review_text']
                ))
                reviews_count += 1
        
        connection.commit()
        print(f"✓ {reviews_count} sample reviews inserted successfully")
        
        # Update movie ratings based on reviews
        cursor.execute("""
            UPDATE movies m
            SET rating = (
                SELECT AVG(r.rating)
                FROM reviews r
                WHERE r.movie_id = m.id
            ),
            total_reviews = (
                SELECT COUNT(r.id)
                FROM reviews r
                WHERE r.movie_id = m.id
            )
        """)
        
        connection.commit()
        print("✓ Movie ratings updated successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Error inserting reviews: {err}")
        return False
    
    finally:
        cursor.close()
        connection.close()

def create_static_directories():
    """Create static directories for assets"""
    directories = [
        'static',
        'static/css',
        'static/js',
        'static/images',
        'static/images/movies'
    ]
    
    for directory in directories:
        full_path = os.path.join(os.path.dirname(__file__), directory)
        os.makedirs(full_path, exist_ok=True)
        print(f"✓ Directory '{directory}' created")

def main():
    """Main initialization function"""
    print("=" * 50)
    print("MovieHub Database Initialization")
    print("=" * 50)
    
    # Create static directories
    print("\n1. Creating static directories...")
    create_static_directories()
    
    # Create database
    print("\n2. Creating database...")
    if not create_database():
        print("✗ Failed to create database. Exiting.")
        return
    
    # Create tables
    print("\n3. Creating tables...")
    if not create_tables():
        print("✗ Failed to create tables. Exiting.")
        return
    
    # Insert sample data
    print("\n4. Inserting sample data...")
    
    print("   4.1 Inserting sample movies...")
    insert_sample_movies()
    
    print("   4.2 Inserting sample theaters...")
    insert_sample_theaters()
    
    print("   4.3 Inserting sample shows...")
    insert_sample_shows()
    
    print("   4.4 Inserting sample reviews...")
    insert_sample_reviews()
    
    print("\n" + "=" * 50)
    print("✓ Database initialization completed successfully!")
    print("=" * 50)
    print("\nYou can now run the application with: python app.py")
    print("\nDefault admin access: http://localhost:5000/admin")
    print("Sample data includes:")
    print("• 6 sample movies")
    print("• 4 sample theaters") 
    print("• Multiple shows for the next 7 days")
    print("• Sample customer reviews")

if __name__ == "__main__":
    main()