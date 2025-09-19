from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
from datetime import datetime, timedelta
import traceback

app = Flask(__name__)
app.secret_key = 'moviehub-secret-key'

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value)
    except:
        return []

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Internal server error. Please try again later."), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message="Page not found."), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    print(f"Error: {str(e)}")
    print(traceback.format_exc())
    return render_template('error.html', message="An unexpected error occurred."), 500

class MovieData:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        if hasattr(self, 'release_date') and isinstance(self.release_date, str):
            self.release_date = datetime.strptime(self.release_date, '%Y-%m-%d').date()
        if not hasattr(self, 'rating'):
            self.rating = getattr(self, 'avg_rating', 0)

# Sample data - no database needed
MOVIES_DATA = [
    {
        'id': 1,
        'title': 'Avengers: Endgame',
        'description': 'After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos.',
        'duration': 181,
        'genre': 'Action',
        'language': 'English',
        'release_date': '2019-04-26',
        'image_url': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg',
        'avg_rating': 4.8,
        'review_count': 1250
    },
    {
        'id': 2,
        'title': 'Spider-Man: No Way Home',
        'description': 'Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero.',
        'duration': 148,
        'genre': 'Action',
        'language': 'English',
        'release_date': '2021-12-17',
        'image_url': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg',
        'avg_rating': 4.7,
        'review_count': 980
    },
    {
        'id': 3,
        'title': 'The Dark Knight',
        'description': 'Batman raises the stakes in his war on crime with the help of Lt. Jim Gordon and District Attorney Harvey Dent.',
        'duration': 152,
        'genre': 'Action',
        'language': 'English',
        'release_date': '2008-07-18',
        'image_url': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
        'avg_rating': 4.9,
        'review_count': 2100
    }
]

MOVIES = [MovieData(movie) for movie in MOVIES_DATA]

SHOWS = [
    {'id': 1, 'movie_id': 1, 'title': 'Avengers: Endgame', 'theater_name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'show_date': datetime(2024, 1, 15).date(), 'show_time': datetime.strptime('19:30:00', '%H:%M:%S').time(), 'price': 250, 'available_seats': 85},
    {'id': 2, 'movie_id': 1, 'title': 'Avengers: Endgame', 'theater_name': 'INOX Multiplex', 'location': 'R City Mall, Mumbai', 'show_date': datetime(2024, 1, 15).date(), 'show_time': datetime.strptime('22:00:00', '%H:%M:%S').time(), 'price': 300, 'available_seats': 92},
    {'id': 3, 'movie_id': 2, 'title': 'Spider-Man: No Way Home', 'theater_name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'show_date': datetime(2024, 1, 16).date(), 'show_time': datetime.strptime('16:00:00', '%H:%M:%S').time(), 'price': 280, 'available_seats': 78}
]

REVIEWS = [
    {'id': 1, 'movie_id': 1, 'customer_name': 'John Doe', 'rating': 5, 'review_text': 'Amazing movie! Great storyline and excellent acting.', 'created_at': datetime(2024, 1, 10)},
    {'id': 2, 'movie_id': 1, 'customer_name': 'Jane Smith', 'rating': 4, 'review_text': 'Really enjoyed watching this. Worth the money!', 'created_at': datetime(2024, 1, 12)},
    {'id': 3, 'movie_id': 2, 'customer_name': 'Mike Johnson', 'rating': 5, 'review_text': 'Best Spider-Man movie ever made!', 'created_at': datetime(2024, 1, 11)}
]

@app.route('/')
def home():
    try:
        return render_template('home.html', movies=MOVIES_DATA)
    except Exception as e:
        print(f"Error in home: {str(e)}")
        return render_template('error.html', message="Error loading home page")

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    try:
        movie = next((m for m in MOVIES_DATA if m['id'] == movie_id), None)
        if not movie:
            return render_template('error.html', message="Movie not found")
        
        shows = [s for s in SHOWS if s['movie_id'] == movie_id]
        reviews = [r for r in REVIEWS if r['movie_id'] == movie_id]
        
        return render_template('movie_details.html', movie=movie, shows=shows, reviews=reviews)
    except Exception as e:
        print(f"Error in movie_details: {str(e)}")
        return render_template('error.html', message="Error loading movie details")

@app.route('/book/<int:show_id>')
def book_seats(show_id):
    try:
        show = next((s for s in SHOWS if s['id'] == show_id), None)
        if not show:
            return render_template('error.html', message="Show not found")
        
        movie = next((m for m in MOVIES_DATA if m['id'] == show['movie_id']), None)
        show.update({'title': movie['title'], 'duration': movie['duration'], 'total_seats': 100})
        
        return render_template('book_seats.html', show=show, booked_seats=['A1', 'A2', 'B5'])
    except Exception as e:
        print(f"Error in book_seats: {str(e)}")
        return render_template('error.html', message="Error loading booking page")

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    return jsonify({'success': True, 'booking_id': 12345})

@app.route('/booking_success/<int:booking_id>')
def booking_success(booking_id):
    try:
        booking = {
            'id': booking_id,
            'customer_name': 'Demo User',
            'customer_email': 'demo@example.com',
            'customer_phone': '+91 9876543210',
            'seats_booked': 2,
            'seat_numbers': '["C3", "C4"]',
            'total_amount': 500,
            'show_date': datetime(2024, 1, 15).date(),
            'show_time': datetime.strptime('19:30:00', '%H:%M:%S').time(),
            'title': 'Avengers: Endgame',
            'theater_name': 'PVR Cinemas',
            'location': 'Phoenix Mall, Mumbai',
            'price': 250
        }
        return render_template('booking_success.html', booking=booking)
    except Exception as e:
        print(f"Error in booking_success: {str(e)}")
        return render_template('error.html', message="Error loading booking confirmation")

@app.route('/add_review', methods=['POST'])
def add_review():
    return jsonify({'success': True})

@app.route('/admin')
def admin_dashboard():
    try:
        return render_template('admin/dashboard.html', datetime=datetime)
    except Exception as e:
        print(f"Error in admin_dashboard: {str(e)}")
        return render_template('error.html', message="Error loading admin dashboard")

@app.route('/admin/movies')
def admin_movies():
    try:
        return render_template('admin/movies.html', movies=MOVIES)
    except Exception as e:
        print(f"Error in admin_movies: {str(e)}")
        return render_template('error.html', message="Error loading movies page")

@app.route('/admin/theaters')
def admin_theaters():
    try:
        theaters = [
            {'id': 1, 'name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'total_seats': 120, 'created_at': datetime.now()},
            {'id': 2, 'name': 'INOX Multiplex', 'location': 'R City Mall, Mumbai', 'total_seats': 150, 'created_at': datetime.now()}
        ]
        return render_template('admin/theaters.html', theaters=theaters)
    except Exception as e:
        print(f"Error in admin_theaters: {str(e)}")
        return render_template('error.html', message="Error loading theaters page")

@app.route('/admin/shows')
def admin_shows():
    try:
        theaters = [
            {'id': 1, 'name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'total_seats': 120, 'created_at': datetime.now()},
            {'id': 2, 'name': 'INOX Multiplex', 'location': 'R City Mall, Mumbai', 'total_seats': 150, 'created_at': datetime.now()}
        ]
        return render_template('admin/shows.html', shows=SHOWS, movies=MOVIES_DATA, theaters=theaters)
    except Exception as e:
        print(f"Error in admin_shows: {str(e)}")
        return render_template('error.html', message="Error loading shows page")

@app.route('/admin/bookings')
def admin_bookings():
    try:
        bookings = [
            {'id': 1, 'customer_name': 'Demo User', 'customer_email': 'demo@example.com', 'customer_phone': '+91 9876543210', 'seats_booked': 2, 'total_amount': 500, 'title': 'Avengers: Endgame', 'theater_name': 'PVR Cinemas', 'show_date': datetime(2024, 1, 15).date(), 'show_time': datetime.strptime('19:30:00', '%H:%M:%S').time(), 'booking_date': datetime.now(), 'status': 'confirmed', 'seat_numbers': '["C3", "C4"]'}
        ]
        return render_template('admin/bookings.html', bookings=bookings)
    except Exception as e:
        print(f"Error in admin_bookings: {str(e)}")
        return render_template('error.html', message="Error loading bookings page")

# Add missing admin routes
@app.route('/admin/add_movie', methods=['POST'])
def add_movie():
    flash('Demo mode: Movie would be added in production', 'success')
    return redirect(url_for('admin_movies'))

@app.route('/admin/add_theater', methods=['POST'])
def add_theater():
    flash('Demo mode: Theater would be added in production', 'success')
    return redirect(url_for('admin_theaters'))

@app.route('/admin/add_show', methods=['POST'])
def add_show():
    flash('Demo mode: Show would be added in production', 'success')
    return redirect(url_for('admin_shows'))

if __name__ == '__main__':
    app.run(debug=True)