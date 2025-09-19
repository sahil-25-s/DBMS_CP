from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'moviehub-secret-key'

# Sample data - no database needed
MOVIES = [
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

SHOWS = [
    {'id': 1, 'movie_id': 1, 'theater_name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'show_date': '2024-01-15', 'show_time': '19:30:00', 'price': 250, 'available_seats': 85},
    {'id': 2, 'movie_id': 1, 'theater_name': 'INOX Multiplex', 'location': 'R City Mall, Mumbai', 'show_date': '2024-01-15', 'show_time': '22:00:00', 'price': 300, 'available_seats': 92},
    {'id': 3, 'movie_id': 2, 'theater_name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'show_date': '2024-01-16', 'show_time': '16:00:00', 'price': 280, 'available_seats': 78}
]

REVIEWS = [
    {'id': 1, 'movie_id': 1, 'customer_name': 'John Doe', 'rating': 5, 'review_text': 'Amazing movie! Great storyline and excellent acting.', 'created_at': '2024-01-10'},
    {'id': 2, 'movie_id': 1, 'customer_name': 'Jane Smith', 'rating': 4, 'review_text': 'Really enjoyed watching this. Worth the money!', 'created_at': '2024-01-12'},
    {'id': 3, 'movie_id': 2, 'customer_name': 'Mike Johnson', 'rating': 5, 'review_text': 'Best Spider-Man movie ever made!', 'created_at': '2024-01-11'}
]

@app.route('/')
def home():
    return render_template('home.html', movies=MOVIES)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        return render_template('error.html', message="Movie not found")
    
    shows = [s for s in SHOWS if s['movie_id'] == movie_id]
    reviews = [r for r in REVIEWS if r['movie_id'] == movie_id]
    
    return render_template('movie_details.html', movie=movie, shows=shows, reviews=reviews)

@app.route('/book/<int:show_id>')
def book_seats(show_id):
    show = next((s for s in SHOWS if s['id'] == show_id), None)
    if not show:
        return render_template('error.html', message="Show not found")
    
    movie = next((m for m in MOVIES if m['id'] == show['movie_id']), None)
    show.update({'title': movie['title'], 'duration': movie['duration'], 'total_seats': 100})
    
    return render_template('book_seats.html', show=show, booked_seats=['A1', 'A2', 'B5'])

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    return jsonify({'success': True, 'booking_id': 12345})

@app.route('/booking_success/<int:booking_id>')
def booking_success(booking_id):
    booking = {
        'id': booking_id,
        'customer_name': 'Demo User',
        'customer_email': 'demo@example.com',
        'customer_phone': '+91 9876543210',
        'seats_booked': 2,
        'seat_numbers': '["C3", "C4"]',
        'total_amount': 500,
        'show_date': '2024-01-15',
        'show_time': '19:30:00',
        'title': 'Avengers: Endgame',
        'theater_name': 'PVR Cinemas',
        'location': 'Phoenix Mall, Mumbai',
        'price': 250
    }
    return render_template('booking_success.html', booking=booking)

@app.route('/add_review', methods=['POST'])
def add_review():
    return jsonify({'success': True})

@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html', datetime=datetime)

@app.route('/admin/movies')
def admin_movies():
    return render_template('admin/movies.html', movies=MOVIES)

@app.route('/admin/theaters')
def admin_theaters():
    theaters = [
        {'id': 1, 'name': 'PVR Cinemas', 'location': 'Phoenix Mall, Mumbai', 'total_seats': 120},
        {'id': 2, 'name': 'INOX Multiplex', 'location': 'R City Mall, Mumbai', 'total_seats': 150}
    ]
    return render_template('admin/theaters.html', theaters=theaters)

@app.route('/admin/shows')
def admin_shows():
    return render_template('admin/shows.html', shows=SHOWS, movies=MOVIES, theaters=[])

@app.route('/admin/bookings')
def admin_bookings():
    bookings = [
        {'id': 1, 'customer_name': 'Demo User', 'customer_email': 'demo@example.com', 'seats_booked': 2, 'total_amount': 500, 'title': 'Avengers: Endgame', 'theater_name': 'PVR Cinemas'}
    ]
    return render_template('admin/bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)