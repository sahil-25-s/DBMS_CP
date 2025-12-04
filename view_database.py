import sqlite3
import pandas as pd

def view_database():
    conn = sqlite3.connect('movienight.db')
    
    # Get all table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== MOVIENIGHT DATABASE ===\n")
    print(f"Tables found: {len(tables)}")
    
    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name.upper()} TABLE ---")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("Columns:", [col[1] for col in columns])
        
        # Get data
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(f"Rows: {len(df)}")
        print(df.to_string(index=False))
        print("-" * 50)
    
    conn.close()

if __name__ == "__main__":
    view_database()