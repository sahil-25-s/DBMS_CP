# MovieHub - Online Movie Booking System

A production-ready web application for online movie ticket booking built with Flask and MySQL.

## Features
- Movie listings with details and reviews
- Interactive seat selection and booking
- Admin panel for managing movies, theaters, and shows
- Responsive design
- SQL-based data persistence

## Architecture
- **models.py**: Database models and operations
- **controllers.py**: Business logic and request handling
- **routes.py**: URL routing with Flask blueprints
- **app.py**: Application factory and configuration
- **config.py**: Environment-specific configurations

## Local Development
1. Copy `.env.example` to `.env` and configure your database
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Visit `http://localhost:5000`
5. Initialize database: `http://localhost:5000/init-db`

## Production Deployment (Vercel)
1. Set environment variables in Vercel dashboard:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`
   - `SECRET_KEY`
2. Deploy to Vercel
3. Initialize database: `https://your-app.vercel.app/init-db`

## Environment Variables
See `.env.example` for required configuration variables.