# Simple in-memory database
movies_db = []
theaters_db = []
shows_db = []
bookings_db = []
reviews_db = []

class Movie:
    @staticmethod
    def get_all():
        return movies_db
    
    @staticmethod
    def get_by_id(movie_id):
        for movie in movies_db:
            if movie['id'] == movie_id:
                return movie
        return None
    
    @staticmethod
    def create(data):
        movie = {
            'id': len(movies_db) + 1,
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'duration': int(data.get('duration', 0)) if data.get('duration') else 0,
            'genre': data.get('genre', ''),
            'language': data.get('language', ''),
            'release_date': data.get('release_date'),
            'image_url': data.get('image_url', ''),
            'created_at': '2024-01-01'
        }
        movies_db.append(movie)
        return True

class Theater:
    @staticmethod
    def get_all():
        return theaters_db
    
    @staticmethod
    def create(data):
        theater = {
            'id': len(theaters_db) + 1,
            'name': data.get('name', ''),
            'location': data.get('location', ''),
            'total_seats': int(data.get('total_seats', 100)),
            'created_at': '2024-01-01'
        }
        theaters_db.append(theater)
        return True

class Show:
    @staticmethod
    def get_all():
        return shows_db
    
    @staticmethod
    def create(data):
        show = {
            'id': len(shows_db) + 1,
            'movie_id': data.get('movie_id'),
            'theater_id': data.get('theater_id'),
            'show_date': data.get('show_date'),
            'show_time': data.get('show_time'),
            'price': float(data.get('price', 0)),
            'available_seats': 100,
            'created_at': '2024-01-01'
        }
        shows_db.append(show)
        return True

class Booking:
    @staticmethod
    def get_all():
        return bookings_db

class Review:
    @staticmethod
    def get_by_movie_id(movie_id):
        return []

class Database:
    @staticmethod
    def init_database():
        return True
    
    @staticmethod
    def get_connection():
        return True