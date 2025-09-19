from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Sample data without database
    movies = [
        {
            'id': 1,
            'title': 'Avengers: Endgame',
            'description': 'Epic superhero movie',
            'genre': 'Action',
            'duration': 181,
            'language': 'English',
            'avg_rating': 4.8,
            'review_count': 1250,
            'image_url': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg'
        },
        {
            'id': 2,
            'title': 'Spider-Man: No Way Home',
            'description': 'Multiverse adventure',
            'genre': 'Action',
            'duration': 148,
            'language': 'English',
            'avg_rating': 4.7,
            'review_count': 980,
            'image_url': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg'
        }
    ]
    return render_template('home.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True, port=5000)