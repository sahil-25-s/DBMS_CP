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

# Initialize database on startup
try:
    from models import Database
    Database.init_database()
except:
    from sqlite_models import Database
    Database.init_database()

if __name__ == '__main__':
    app.run(debug=True, port=5000)