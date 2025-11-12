from flask import Flask, request, session
import os
from dotenv import load_dotenv
from routes import main_bp, admin_bp, api_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

# Initialize SQLite database
import simple_sqlite as db
db.init_database()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎬 MovieNight - Movie Booking System")
    print("="*50)
    print("🌐 Server running at: http://localhost:5000")
    print("⚙️  Admin Panel: http://localhost:5000/admin")
    print("🗄️  Database: SQLite (movienight.db)")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')