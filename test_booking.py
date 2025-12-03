import simple_sqlite as db

# Test the exact same code as in the controller
try:
    show_id = 1
    show_data = db.get_show_by_id(show_id)
    print("Show data:", show_data)
    
    if not show_data:
        print("Show not found")
    else:
        show = {
            'id': show_data[0],
            'movie_id': show_data[1],
            'theater_id': show_data[2],
            'show_date': show_data[3],
            'show_time': show_data[4],
            'price': show_data[5],
            'available_seats': show_data[6],
            'title': show_data[7],
            'theater_name': show_data[8]
        }
        print("Show object:", show)
        
        booked_seats = db.get_booked_seats(show_id)
        print("Booked seats:", booked_seats)
        print("SUCCESS - No errors in booking logic")
        
except Exception as e:
    print("ERROR:", str(e))
    import traceback
    traceback.print_exc()