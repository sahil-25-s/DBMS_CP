from flask import Blueprint
from controllers import MovieController, BookingController, ReviewController, AdminController, DatabaseController

# Create blueprints
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Main routes
@main_bp.route('/')
def index():
    return MovieController.index()

@main_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    return MovieController.details(movie_id)

@main_bp.route('/book_seats/<int:show_id>')
def book_seats(show_id):
    return BookingController.book_seats(show_id)

@main_bp.route('/booking_success/<int:booking_id>')
def booking_success(booking_id):
    return BookingController.booking_success(booking_id)

@main_bp.route('/init-db')
def init_db():
    return DatabaseController.init_db()

# API routes
@api_bp.route('/book_tickets', methods=['POST'])
def book_tickets():
    return BookingController.create_booking()

@api_bp.route('/add_review', methods=['POST'])
def add_review():
    return ReviewController.add_review()

# Admin routes
@admin_bp.route('/')
def dashboard():
    return AdminController.dashboard()

@admin_bp.route('/movies')
def movies():
    return AdminController.movies()

@admin_bp.route('/theaters')
def theaters():
    return AdminController.theaters()

@admin_bp.route('/shows')
def shows():
    return AdminController.shows()

@admin_bp.route('/bookings')
def bookings():
    return AdminController.bookings()

@admin_bp.route('/add_movie', methods=['POST'])
def add_movie():
    return AdminController.add_movie()

@admin_bp.route('/add_theater', methods=['POST'])
def add_theater():
    return AdminController.add_theater()

@admin_bp.route('/add_show', methods=['POST'])
def add_show():
    return AdminController.add_show()