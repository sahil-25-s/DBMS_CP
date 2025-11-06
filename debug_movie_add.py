#!/usr/bin/env python3
"""
Debug script to identify the movie addition issue
"""
import os
import mysql.connector
from dotenv import load_dotenv
from models import Database, Movie

# Load environment variables from .env file
print(f"Loading .env from: {os.path.abspath('.env')}")
load_dotenv()
print(f"Environment loaded. DB_PASSWORD exists: {bool(os.environ.get('DB_PASSWORD'))}")

def test_database_connection():
    """Test database connection"""
    print("=== Testing Database Connection ===")
    
    # Print environment variables
    print(f"DB_HOST: {os.environ.get('DB_HOST', 'localhost')}")
    print(f"DB_USER: {os.environ.get('DB_USER', 'root')}")
    db_password = os.environ.get('DB_PASSWORD')
    print(f"DB_PASSWORD: {'***' if db_password else 'Not set'}")
    print(f"DB_PASSWORD length: {len(db_password) if db_password else 0}")
    print(f"DB_PASSWORD value: '{db_password}'")
    print(f"DB_NAME: {os.environ.get('DB_NAME', 'moviehub')}")
    print(f"DB_PORT: {os.environ.get('DB_PORT', 3306)}")
    
    try:
        connection = Database.get_connection()
        if connection:
            print("[OK] Database connection successful")
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"[OK] MySQL version: {version[0]}")
            cursor.close()
            connection.close()
            return True
        else:
            print("[FAIL] Database connection failed")
            return False
    except Exception as e:
        print(f"[FAIL] Database connection error: {e}")
        return False

def test_table_exists():
    """Test if movies table exists"""
    print("\n=== Testing Movies Table ===")
    
    try:
        connection = Database.get_connection()
        if not connection:
            print("[FAIL] Cannot connect to database")
            return False
            
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'movies'")
        result = cursor.fetchone()
        
        if result:
            print("[OK] Movies table exists")
            
            # Check table structure
            cursor.execute("DESCRIBE movies")
            columns = cursor.fetchall()
            print("Table structure:")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("[FAIL] Movies table does not exist")
            cursor.close()
            connection.close()
            return False
            
    except Exception as e:
        print(f"[FAIL] Error checking table: {e}")
        return False

def test_movie_creation():
    """Test movie creation with sample data"""
    print("\n=== Testing Movie Creation ===")
    
    sample_data = {
        'title': 'Test Movie',
        'description': 'This is a test movie for debugging',
        'duration': '120',
        'genre': 'Action',
        'language': 'English',
        'release_date': '2024-01-01',
        'image_url': 'https://example.com/poster.jpg'
    }
    
    print("Sample data:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    try:
        result = Movie.create(sample_data)
        if result:
            print("[OK] Movie creation successful")
            return True
        else:
            print("[FAIL] Movie creation failed")
            return False
    except Exception as e:
        print(f"[FAIL] Movie creation error: {e}")
        return False

def main():
    print("MovieHub Debug Script")
    print("=" * 50)
    
    # Check if .env file exists
    env_path = os.path.abspath('.env')
    print(f"Checking .env file at: {env_path}")
    print(f".env file exists: {os.path.exists(env_path)}")
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            print("Contents of .env file:")
            print(f.read())
    print()
    
    # Test database connection
    if not test_database_connection():
        print("\n[ERROR] Database connection failed. Please check your .env file and database server.")
        return
    
    # Test table existence
    if not test_table_exists():
        print("\n[ERROR] Movies table missing. Run /init-db endpoint to create tables.")
        return
    
    # Test movie creation
    if not test_movie_creation():
        print("\n[ERROR] Movie creation failed. Check the detailed error above.")
        return
    
    print("\n[SUCCESS] All tests passed! The movie addition should work.")

if __name__ == "__main__":
    main()