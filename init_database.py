import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        db_name = os.environ.get('DB_NAME', 'movienight')
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    create_database()