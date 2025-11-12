from flask import render_template, request, jsonify, flash, redirect
from datetime import datetime
try:
    from models import Movie, Theater, Show, Booking, Review, Database
except:
    from sqlite_models import Movie, Theater, Show, Booking, Review, Database

class MovieController:
    @staticmethod
    def index():
        from sqlite_models import Movie
        movies = Movie.get_all()
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
        from sqlite_models import Movie
        movies = Movie.get_all()
        return render_template('admin/movies.html', movies=movies)
    
    @staticmethod
    def theaters():
        from sqlite_models import Theater
        theaters = Theater.get_all()
        return render_template('admin/theaters.html', theaters=theaters)
    
    @staticmethod
    def shows():
        from sqlite_models import Show, Movie, Theater
        shows = Show.get_all()
        movies = Movie.get_all()
        theaters = Theater.get_all()
        return render_template('admin/shows.html', 
                             shows=shows, movies=movies, theaters=theaters)
    
    @staticmethod
    def bookings():
        bookings = Booking.get_all()
        return render_template('admin/bookings.html', bookings=bookings)
    
    @staticmethod
    def add_movie():
        from sqlite_models import Movie
        
        try:
            data = request.form
            success = Movie.create(data)
            
            if success:
                flash('Movie added successfully!', 'success')
            else:
                flash('Failed to add movie', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect('/admin/movies')
    
    @staticmethod
    def add_theater():
        from sqlite_models import Theater
        
        try:
            data = request.form
            success = Theater.create(data)
            
            if success:
                flash('Theater added successfully!', 'success')
            else:
                flash('Failed to add theater', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect('/admin/theaters')
    
    @staticmethod
    def add_show():
        from sqlite_models import Show
        
        try:
            data = request.form
            success = Show.create(data)
            
            if success:
                flash('Show added successfully!', 'success')
            else:
                flash('Failed to add show', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return redirect('/admin/shows')

class DatabaseController:
    @staticmethod
    def init_db():
        from sqlite_models import Database
        success = Database.init_database()
        if success:
            return jsonify({'success': True, 'message': 'Database initialized successfully'})
        else:
            return jsonify({'success': False, 'message': 'Database initialization failed'})