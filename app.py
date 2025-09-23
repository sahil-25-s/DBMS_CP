from flask import Flask
import os
from routes import main_bp, admin_bp, api_bp
from models import Database

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    # Initialize database for local development
    if os.environ.get('DB_HOST') == 'localhost':
        Database.init_database()
    app.run(debug=True, port=5000)