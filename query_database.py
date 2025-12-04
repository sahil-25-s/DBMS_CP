import sqlite3

def run_query(query):
    conn = sqlite3.connect('movienight.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            # Get column names
            columns = [description[0] for description in cursor.description]
            print("Columns:", columns)
            for row in results:
                print(row)
        else:
            conn.commit()
            print("Query executed successfully")
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()

# Example queries
if __name__ == "__main__":
    print("=== SAMPLE QUERIES ===\n")
    
    print("1. All movies:")
    run_query("SELECT * FROM movies")
    
    print("\n2. All bookings with movie titles:")
    run_query("""SELECT b.id, b.customer_name, m.title, b.seat_numbers, b.total_amount 
                 FROM bookings b 
                 JOIN shows s ON b.show_id = s.id 
                 JOIN movies m ON s.movie_id = m.id""")
    
    print("\n3. Food items by category:")
    run_query("SELECT category, name, price FROM food_items ORDER BY category, price")
    
    print("\n4. Available seats per show:")
    run_query("""SELECT m.title, t.name, s.show_date, s.show_time, s.available_seats 
                 FROM shows s 
                 JOIN movies m ON s.movie_id = m.id 
                 JOIN theaters t ON s.theater_id = t.id""")