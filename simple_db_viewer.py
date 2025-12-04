import sqlite3

def view_database():
    conn = sqlite3.connect('movienight.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=== MOVIENIGHT DATABASE ===\n")
    print(f"Tables: {[t[0] for t in tables]}\n")
    
    for table in tables:
        table_name = table[0]
        print(f"--- {table_name.upper()} ---")
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        print(f"Columns: {columns}")
        print(f"Rows: {len(rows)}")
        
        for row in rows:
            print(row)
        print()
    
    conn.close()

if __name__ == "__main__":
    view_database()