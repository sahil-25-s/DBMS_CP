from flask import Flask, request, session
import os
from dotenv import load_dotenv
from flask_babel import Babel, get_locale
try:
    from models import Database
except:
    from sqlite_models import Database
from routes import main_bp, admin_bp, api_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Babel configuration
app.config['LANGUAGES'] = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'hi': 'हिन्दी',
    'ja': '日本語'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel(app)

@babel.localeselector
def get_locale():
    # 1. Check if language is set in session
    if 'language' in session:
        return session['language']
    # 2. Check Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    # Initialize database for local development
    if os.environ.get('DB_HOST') == 'localhost':
        Database.init_database()
    app.run(debug=True, port=5000)