from flask import Flask
import os
from models import Database
from controllers import MovieController, BookingController, ReviewController, AdminController, DatabaseController

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Main routes
@app.route('/')
def index():
    return MovieController.index()

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    return MovieController.details(movie_id)

@app.route('/book_seats/<int:show_id>')
def book_seats(show_id):
    return BookingController.book_seats(show_id)

@app.route('/booking_success/<int:booking_id>')
def booking_success(booking_id):
    return BookingController.booking_success(booking_id)

@app.route('/init-db')
def init_db():
    return DatabaseController.init_db()

# API routes
@app.route('/api/book_tickets', methods=['POST'])
def book_tickets():
    return BookingController.create_booking()

@app.route('/api/add_review', methods=['POST'])
def add_review():
    return ReviewController.add_review()

# Admin routes
@app.route('/admin/')
def admin_dashboard():
    return AdminController.dashboard()

@app.route('/admin/movies')
def admin_movies():
    return AdminController.movies()

@app.route('/admin/theaters')
def admin_theaters():
    return AdminController.theaters()

@app.route('/admin/shows')
def admin_shows():
    return AdminController.shows()

@app.route('/admin/bookings')
def admin_bookings():
    return AdminController.bookings()

@app.route('/admin/add_movie', methods=['POST'])
def add_movie():
    return AdminController.add_movie()

@app.route('/admin/add_theater', methods=['POST'])
def add_theater():
    return AdminController.add_theater()

@app.route('/admin/add_show', methods=['POST'])
def add_show():
    return AdminController.add_show()

if __name__ == '__main__':
    # Initialize database for local development
    if os.environ.get('DB_HOST') == 'localhost':
        Database.init_database()
    app.run(debug=True, port=5000)