# MovieHub - Online Movie Booking System

A comprehensive web application for online movie ticket booking, similar to BookMyShow, built with Flask, MySQL, HTML, CSS, and JavaScript.

## Features

### 🎬 Customer Features
- **Movie Listings**: Browse latest movies with detailed information
- **Interactive Seat Selection**: Choose your preferred seats with visual seat map
- **Guest Booking**: Book tickets without user registration
- **Multiple Theaters**: Select from various theater locations
- **Show Times**: View available shows with dates and timings
- **Reviews & Ratings**: Read and write movie reviews
- **Booking Confirmation**: Get detailed booking confirmation with ticket information
- **Simulated Payment**: Secure payment simulation process

### 🛠️ Admin Features
- **Movie Management**: Add, edit, and manage movie listings
- **Theater Management**: Manage theater locations and seating capacity
- **Show Scheduling**: Schedule movies across different theaters and time slots
- **Booking Management**: View and manage customer bookings
- **Dashboard**: Comprehensive admin dashboard with statistics

### 🎨 Technical Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Real-time Seat Availability**: Dynamic seat booking with real-time updates
- **Search & Filter**: Advanced search and filtering capabilities
- **Accessibility**: Keyboard navigation and screen reader support
- **Performance Optimized**: Lazy loading, caching, and optimized assets

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Icons**: Font Awesome
- **Architecture**: MVC Pattern

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL 8.0 or higher
- Web browser (Chrome, Firefox, Safari, Edge)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DBMS_CP
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL Database
1. Start your MySQL server
2. Update the database configuration in `app.py`:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_mysql_password',  # Update this
       'database': 'movie_booking_system'
   }
   ```

### 4. Initialize the Database
```bash
python init_db.py
```
This will:
- Create the database and tables
- Insert sample movies, theaters, and shows
- Set up sample reviews and ratings

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
DBMS_CP/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── movie_details.html # Movie details page
│   ├── book_seats.html   # Seat booking page
│   ├── booking_success.html # Booking confirmation
│   ├── error.html        # Error page
│   └── admin/           # Admin templates
│       ├── dashboard.html
│       ├── movies.html
│       ├── theaters.html
│       ├── shows.html
│       └── bookings.html
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Main stylesheet
    ├── js/
    │   └── main.js      # JavaScript functionality
    └── images/          # Image assets
```

## Database Schema

### Tables
1. **movies** - Movie information and metadata
2. **theaters** - Theater locations and seating capacity
3. **shows** - Movie showtimes at specific theaters
4. **bookings** - Customer booking records
5. **reviews** - Customer reviews and ratings

### Key Relationships
- Shows link Movies and Theaters
- Bookings reference Shows
- Reviews reference Movies

## Usage Guide

### For Customers
1. **Browse Movies**: Visit the homepage to see available movies
2. **View Details**: Click on any movie to see details, showtimes, and reviews
3. **Book Tickets**: Select a showtime and choose your seats
4. **Payment**: Complete the simulated payment process
5. **Confirmation**: Get your booking confirmation and ticket details

### For Administrators
1. **Access Admin Panel**: Go to `/admin` or click the Admin link in navigation
2. **Manage Movies**: Add new movies with posters, descriptions, and details
3. **Manage Theaters**: Add theater locations with seating information
4. **Schedule Shows**: Create showtimes by linking movies and theaters
5. **View Bookings**: Monitor customer bookings and generate reports

## API Endpoints

### Public Routes
- `GET /` - Homepage with movie listings
- `GET /movie/<id>` - Movie details page
- `GET /book/<show_id>` - Seat booking page
- `POST /confirm_booking` - Process booking (JSON API)
- `POST /add_review` - Submit movie review (JSON API)
- `GET /booking_success/<booking_id>` - Booking confirmation page

### Admin Routes
- `GET /admin` - Admin dashboard
- `GET /admin/movies` - Movie management
- `GET /admin/theaters` - Theater management
- `GET /admin/shows` - Show scheduling
- `GET /admin/bookings` - Booking management
- `POST /admin/add_movie` - Add new movie
- `POST /admin/add_theater` - Add new theater
- `POST /admin/add_show` - Schedule new show

## Features in Detail

### Seat Selection System
- Visual seat map with rows (A, B, C...) and numbers (1, 2, 3...)
- Real-time seat availability checking
- Maximum 10 seats per booking
- Intuitive color coding (Available, Selected, Booked)
- Keyboard navigation support

### Booking Process
1. **Seat Selection**: Choose seats from interactive map
2. **Customer Details**: Enter name, email, and phone
3. **Payment Simulation**: Select payment method and process
4. **Confirmation**: Receive detailed booking confirmation

### Admin Dashboard
- Statistics overview (movies, theaters, bookings)
- Quick actions for common tasks
- Data management with search and filtering
- Responsive design for all devices

## Customization

### Adding New Movies
Use the admin panel or directly insert into the database:
```python
# Sample movie data structure
movie_data = {
    'title': 'Movie Title',
    'description': 'Movie description...',
    'duration': 120,  # minutes
    'genre': 'Action',
    'language': 'English',
    'release_date': '2024-01-01',
    'image_url': 'https://example.com/poster.jpg'
}
```

### Styling Customization
Modify `static/css/style.css` to customize:
- Color scheme (CSS variables in `:root`)
- Typography and spacing
- Component styles
- Responsive breakpoints

### Adding New Features
1. Update database schema in `init_db.py`
2. Add new routes in `app.py`
3. Create corresponding templates
4. Update CSS and JavaScript as needed

## Security Considerations

- Input validation and sanitization
- SQL injection prevention using parameterized queries
- XSS protection through template escaping
- CSRF protection (implement in production)
- Environment-based configuration for sensitive data

## Performance Optimization

- Database indexing on frequently queried columns
- Image optimization and lazy loading
- CSS and JavaScript minification
- Caching for static assets
- Database connection pooling

## Browser Support

- Chrome 60+ ✅
- Firefox 55+ ✅
- Safari 12+ ✅
- Edge 79+ ✅
- Mobile browsers ✅

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Email: support@moviehub.com
- Create an issue in the repository
- Check the documentation

## Acknowledgments

- Font Awesome for icons
- Movie poster images from The Movie Database (TMDB)
- Flask and MySQL communities
- Bootstrap inspiration for responsive design

---

**MovieHub** - Making movie booking simple and enjoyable! 🎬🍿