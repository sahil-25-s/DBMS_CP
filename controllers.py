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
        movie = Movie.get_by_id(movie_id)
        if not movie:
            return render_template('error.html', message="Movie not found")
        
        shows = Show.get_by_movie_id(movie_id)
        reviews = Review.get_by_movie_id(movie_id)
        
        return render_template('movie_details.html', 
                             movie=movie, shows=shows, reviews=reviews)

class BookingController:
    @staticmethod
    def book_seats(show_id):
        show = Show.get_by_id(show_id)
        if not show:
            return render_template('error.html', message="Show not found")
        
        return render_template('book_seats.html', show=show)
    
    @staticmethod
    def create_booking():
        data = request.json
        booking_id = Booking.create(data)
        
        if booking_id:
            return jsonify({'success': True, 'booking_id': booking_id})
        else:
            return jsonify({'success': False, 'message': 'Booking failed'})
    
    @staticmethod
    def booking_success(booking_id):
        booking = Booking.get_by_id(booking_id)
        if not booking:
            return render_template('error.html', message="Booking not found")
        
        return render_template('booking_success.html', booking=booking)
    
    @staticmethod
    def payment_success():
        return render_template('payment_success.html')
    
    @staticmethod
    def payment_instructions():
        return render_template('payment_instructions.html')

class ReviewController:
    @staticmethod
    def add_review():
        data = request.json
        success = Review.create(data)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Review submission failed'})

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
        bookings = Booking.get_all()
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
            db.add_show(
                data.get('movie_id'),
                data.get('theater_id'),
                data.get('show_date'),
                data.get('show_time'),
                float(data.get('price', 0)),
                100
            )
            flash('Show added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect('/admin/shows')

class DatabaseController:
    @staticmethod
    def init_db():
        return jsonify({'success': True, 'message': 'Database initialized successfully'})