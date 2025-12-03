from flask import render_template, request, jsonify, flash, redirect
from datetime import datetime
import simple_sqlite as db

class MovieController:
    @staticmethod
    def index():
        try:
            rows = db.get_all_movies()
            movies = []
            for row in rows:
                movies.append({
                    'id': row[0], 'title': row[1], 'description': row[2],
                    'duration': row[3], 'genre': row[4], 'language': row[5],
                    'release_date': row[6], 'image_url': row[7]
                })
        except:
            movies = []
        return render_template('home.html', movies=movies)
    
    @staticmethod
    def details(movie_id):
        try:
            rows = db.get_all_movies()
            movie = None
            for row in rows:
                if row[0] == movie_id:
                    movie = {
                        'id': row[0], 'title': row[1], 'description': row[2],
                        'duration': row[3], 'genre': row[4], 'language': row[5],
                        'release_date': row[6], 'image_url': row[7]
                    }
                    break
            
            if not movie:
                return render_template('error.html', message="Movie not found")
            
            # Get shows for this movie
            show_rows = db.get_all_shows()
            shows = []
            for row in show_rows:
                if row[1] == movie_id:  # movie_id is at index 1
                    shows.append({
                        'id': row[0], 'movie_id': row[1], 'theater_id': row[2],
                        'show_date': row[3], 'show_time': row[4], 'price': row[5],
                        'available_seats': row[6], 'title': row[7], 'theater_name': row[8]
                    })
            
            reviews = []
            
            return render_template('movie_details.html', 
                                 movie=movie, shows=shows, reviews=reviews)
        except Exception as e:
            print(f"Error in movie details: {str(e)}")
            return render_template('error.html', message="Movie not found")

class BookingController:
    @staticmethod
    def book_seats(show_id):
        try:
            show_data = db.get_show_by_id(show_id)
            if not show_data:
                return render_template('error.html', message="Show not found")
            
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
            
            booked_seats = db.get_booked_seats(show_id)
            return render_template('book_seats.html', show=show, booked_seats=booked_seats)
        except Exception as e:
            print(f"Error in book_seats: {str(e)}")
            return render_template('error.html', message="Error loading booking page")
    
    @staticmethod
    def create_booking():
        try:
            data = request.get_json()
            
            # Extract booking data
            show_id = data.get('show_id')
            customer_name = data.get('customer_name')
            customer_email = data.get('customer_email')
            customer_phone = data.get('customer_phone')
            selected_seats = data.get('selected_seats', [])
            total_amount = data.get('total_amount')
            
            # Validate required fields
            if not all([show_id, customer_name, customer_email, selected_seats]):
                return jsonify({'success': False, 'message': 'Missing required fields'})
            
            # Create booking in database
            booking_id = db.add_booking(show_id, customer_name, customer_email, 
                                      customer_phone, selected_seats, total_amount)
            
            if booking_id:
                return jsonify({
                    'success': True, 
                    'booking_id': booking_id,
                    'message': 'Booking created successfully'
                })
            else:
                return jsonify({
                    'success': False, 
                    'message': 'Failed to create booking'
                })
            
        except Exception as e:
            return jsonify({
                'success': False, 
                'message': f'Error creating booking: {str(e)}'
            })
    
    @staticmethod
    def booking_success(booking_id):
        try:
            booking_data = db.get_booking_by_id(booking_id)
            if not booking_data:
                return render_template('error.html', message="Booking not found")
            
            import json
            booking = {
                'id': booking_data[0],
                'show_id': booking_data[1],
                'customer_name': booking_data[2],
                'customer_email': booking_data[3],
                'customer_phone': booking_data[4],
                'selected_seats': json.loads(booking_data[5]) if booking_data[5] else [],
                'total_amount': booking_data[6],
                'booking_date': 'Just now',
                'show_date': booking_data[7],
                'show_time': booking_data[8],
                'title': booking_data[9],
                'theater_name': booking_data[10]
            }
            return render_template('booking_success.html', booking=booking)
        except Exception as e:
            print(f"Error in booking_success: {str(e)}")
            return render_template('error.html', message="Error loading booking details")
    
    @staticmethod
    def payment_success():
        return render_template('payment_success.html')
    
    @staticmethod
    def payment_instructions():
        return render_template('payment_instructions.html')

class ReviewController:
    @staticmethod
    def add_review():
        return jsonify({'success': True})

class AdminController:
    @staticmethod
    def dashboard():
        return render_template('admin/dashboard.html', datetime=datetime)
    
    @staticmethod
    def movies():
        try:
            rows = db.get_all_movies()
            movies = []
            for row in rows:
                movies.append({
                    'id': row[0], 'title': row[1], 'description': row[2],
                    'duration': row[3], 'genre': row[4], 'language': row[5],
                    'release_date': row[6], 'image_url': row[7]
                })
        except:
            movies = []
        return render_template('admin/movies.html', movies=movies)
    
    @staticmethod
    def theaters():
        try:
            rows = db.get_all_theaters()
            theaters = []
            for row in rows:
                theaters.append({
                    'id': row[0], 'name': row[1], 'location': row[2], 'total_seats': row[3]
                })
        except:
            theaters = []
        return render_template('admin/theaters.html', theaters=theaters)
    
    @staticmethod
    def shows():
        try:
            show_rows = db.get_all_shows()
            movie_rows = db.get_all_movies()
            theater_rows = db.get_all_theaters()
            
            shows = []
            for row in show_rows:
                shows.append({
                    'id': row[0], 'movie_id': row[1], 'theater_id': row[2],
                    'show_date': row[3], 'show_time': row[4], 'price': row[5],
                    'available_seats': row[6], 'title': row[7], 'theater_name': row[8]
                })
            
            movies = []
            for row in movie_rows:
                movies.append({'id': row[0], 'title': row[1]})
            
            theaters = []
            for row in theater_rows:
                theaters.append({'id': row[0], 'name': row[1], 'location': row[2]})
        except:
            shows, movies, theaters = [], [], []
            
        return render_template('admin/shows.html', shows=shows, movies=movies, theaters=theaters)
    
    @staticmethod
    def bookings():
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''SELECT b.*, s.show_date, s.show_time, m.title, t.name as theater_name
                             FROM bookings b
                             LEFT JOIN shows s ON b.show_id = s.id
                             LEFT JOIN movies m ON s.movie_id = m.id
                             LEFT JOIN theaters t ON s.theater_id = t.id
                             ORDER BY b.booking_date DESC''')
            
            booking_rows = cursor.fetchall()
            conn.close()
            
            import json
            bookings = []
            for row in booking_rows:
                bookings.append({
                    'id': row[0],
                    'show_id': row[1],
                    'customer_name': row[2],
                    'customer_email': row[3],
                    'customer_phone': row[4],
                    'seat_numbers': json.loads(row[5]) if row[5] else [],
                    'total_amount': row[6],
                    'booking_date': row[7],
                    'show_date': row[8],
                    'show_time': row[9],
                    'title': row[10],
                    'theater_name': row[11]
                })
        except:
            bookings = []
        return render_template('admin/bookings.html', bookings=bookings)
    
    @staticmethod
    def add_movie():
        data = request.form
        try:
            db.add_movie(
                data.get('title', ''),
                data.get('description', ''),
                int(data.get('duration', 0)) if data.get('duration') else 0,
                data.get('genre', ''),
                data.get('language', ''),
                data.get('release_date', ''),
                data.get('image_url', '')
            )
            flash('Movie added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect('/admin/movies')
    
    @staticmethod
    def add_theater():
        data = request.form
        try:
            db.add_theater(
                data.get('name', ''),
                data.get('location', ''),
                int(data.get('total_seats', 100))
            )
            flash('Theater added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect('/admin/theaters')
    
    @staticmethod
    def add_show():
        data = request.form
        try:
            print(f"\n🎬 Adding show with data: {dict(data)}")
            db.add_show(
                int(data.get('movie_id')),
                int(data.get('theater_id')),
                data.get('show_date'),
                data.get('show_time'),
                float(data.get('price', 0)),
                100
            )
            flash('Show added successfully!', 'success')
        except Exception as e:
            print(f"❌ Error adding show: {str(e)}")
            flash(f'Error: {str(e)}', 'error')
        return redirect('/admin/shows')

class DatabaseController:
    @staticmethod
    def init_db():
        return jsonify({'success': True, 'message': 'Database initialized successfully'})
    
    @staticmethod
    def update_images():
        try:
            db.update_all_movie_images()
            return jsonify({'success': True, 'message': 'Movie images updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})