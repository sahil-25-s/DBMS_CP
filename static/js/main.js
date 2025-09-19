// ===== MAIN JAVASCRIPT FILE FOR MOVIEHUB =====

// Global variables
let currentUser = null;
let selectedSeats = [];

// ===== UTILITY FUNCTIONS =====

// Format currency
function formatCurrency(amount) {
    return `₹${Math.round(amount)}`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });
}

// Format time
function formatTime(timeString) {
    const time = new Date(`1970-01-01T${timeString}`);
    return time.toLocaleTimeString('en-IN', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Show loading spinner
function showLoading(element, message = 'Loading...') {
    element.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>${message}</p>
        </div>
    `;
}

// Show error message
function showError(element, message) {
    element.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            <p>${message}</p>
        </div>
    `;
}

// Show success message
function showSuccess(message, duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success';
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    flashContainer.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, duration);
}

// Create flash messages container if it doesn't exist
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== NAVIGATION AND MENU =====

// Handle mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Smooth scroll to sections
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ===== MOVIE FUNCTIONALITY =====

// Filter movies by genre
function filterMoviesByGenre(genre) {
    const movieCards = document.querySelectorAll('.movie-card');
    
    movieCards.forEach(card => {
        const movieGenre = card.querySelector('.genre')?.textContent?.trim();
        
        if (!genre || genre === 'all' || movieGenre === genre) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Search movies by title
function searchMovies(query) {
    const movieCards = document.querySelectorAll('.movie-card');
    const searchTerm = query.toLowerCase().trim();
    
    movieCards.forEach(card => {
        const movieTitle = card.querySelector('h3')?.textContent?.toLowerCase();
        const movieDescription = card.querySelector('.movie-description')?.textContent?.toLowerCase();
        
        if (!searchTerm || 
            movieTitle?.includes(searchTerm) || 
            movieDescription?.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ===== SEAT BOOKING FUNCTIONALITY =====

// Initialize seat map
function initializeSeatMap(totalSeats, bookedSeats, seatPrice) {
    const seatMap = document.getElementById('seatMap');
    if (!seatMap) return;

    seatMap.innerHTML = '';
    selectedSeats = [];
    
    const rows = Math.ceil(totalSeats / 10);
    
    for (let row = 0; row < rows; row++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';
        
        // Row label
        const rowLabel = document.createElement('div');
        rowLabel.className = 'row-label';
        rowLabel.textContent = String.fromCharCode(65 + row); // A, B, C...
        rowDiv.appendChild(rowLabel);
        
        // Seats in this row
        for (let seat = 1; seat <= 10; seat++) {
            const seatNumber = row * 10 + seat;
            if (seatNumber > totalSeats) break;
            
            const seatId = `${String.fromCharCode(65 + row)}${seat}`;
            const seatDiv = document.createElement('div');
            seatDiv.className = 'seat';
            seatDiv.dataset.seat = seatId;
            seatDiv.textContent = seat;
            
            if (bookedSeats && bookedSeats.includes(seatId)) {
                seatDiv.classList.add('booked');
            } else {
                seatDiv.classList.add('available');
                seatDiv.addEventListener('click', () => toggleSeatSelection(seatDiv, seatPrice));
            }
            
            rowDiv.appendChild(seatDiv);
        }
        
        seatMap.appendChild(rowDiv);
    }
}

// Toggle seat selection
function toggleSeatSelection(seatElement, seatPrice) {
    const seatId = seatElement.dataset.seat;
    
    if (seatElement.classList.contains('selected')) {
        // Deselect seat
        seatElement.classList.remove('selected');
        seatElement.classList.add('available');
        selectedSeats = selectedSeats.filter(seat => seat !== seatId);
    } else {
        // Select seat (max 10 seats)
        if (selectedSeats.length >= 10) {
            showError(document.body, 'You can select maximum 10 seats at a time');
            return;
        }
        
        seatElement.classList.remove('available');
        seatElement.classList.add('selected');
        selectedSeats.push(seatId);
    }
    
    updateBookingSummary(seatPrice);
}

// Update booking summary
function updateBookingSummary(seatPrice) {
    const summaryDiv = document.getElementById('bookingSummary');
    const customerForm = document.getElementById('customerForm');
    
    if (selectedSeats.length > 0) {
        // Show summary and form
        if (summaryDiv) summaryDiv.style.display = 'block';
        if (customerForm) customerForm.style.display = 'block';
        
        // Update summary details
        const selectedSeatsText = document.getElementById('selectedSeatsText');
        const seatCount = document.getElementById('seatCount');
        const totalAmount = document.getElementById('totalAmount');
        const selectedSeatsInput = document.getElementById('selectedSeats');
        const totalPriceInput = document.getElementById('totalPrice');
        
        if (selectedSeatsText) selectedSeatsText.textContent = selectedSeats.join(', ');
        if (seatCount) seatCount.textContent = selectedSeats.length;
        if (totalAmount) totalAmount.textContent = formatCurrency(selectedSeats.length * seatPrice);
        if (selectedSeatsInput) selectedSeatsInput.value = JSON.stringify(selectedSeats);
        if (totalPriceInput) totalPriceInput.value = selectedSeats.length * seatPrice;
    } else {
        // Hide summary and form
        if (summaryDiv) summaryDiv.style.display = 'none';
        if (customerForm) customerForm.style.display = 'none';
    }
}

// Clear seat selection
function clearSeatSelection() {
    selectedSeats = [];
    document.querySelectorAll('.seat.selected').forEach(seat => {
        seat.classList.remove('selected');
        seat.classList.add('available');
    });
    updateBookingSummary(0);
}

// ===== BOOKING PROCESS =====

// Handle booking form submission
async function handleBookingSubmission(formData, showId, totalAmount) {
    const bookingData = {
        show_id: parseInt(showId),
        customer_name: formData.get('customer_name'),
        customer_email: formData.get('customer_email'),
        customer_phone: formData.get('customer_phone'),
        selected_seats: selectedSeats,
        total_amount: totalAmount
    };
    
    try {
        const response = await fetch('/confirm_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            return result.booking_id;
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        throw new Error('Failed to process booking: ' + error.message);
    }
}

// Show payment modal
function showPaymentModal(bookingData) {
    const modal = document.getElementById('paymentModal');
    if (!modal) return;
    
    // Update payment summary
    const paymentSeats = document.getElementById('paymentSeats');
    const paymentTotal = document.getElementById('paymentTotal');
    
    if (paymentSeats) paymentSeats.textContent = selectedSeats.join(', ');
    if (paymentTotal) paymentTotal.textContent = formatCurrency(bookingData.total_amount);
    
    modal.style.display = 'block';
}

// Process payment (simulated)
async function processPayment(bookingData) {
    const modal = document.getElementById('paymentModal');
    if (!modal) return;
    
    // Show processing state
    const modalContent = modal.querySelector('.modal-content');
    modalContent.innerHTML = `
        <div class="payment-processing">
            <div class="loading-spinner"></div>
            <h3>Processing Payment...</h3>
            <p>Please wait while we confirm your booking.</p>
        </div>
    `;
    
    try {
        // Simulate payment processing delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const bookingId = await handleBookingSubmission(bookingData.formData, bookingData.showId, bookingData.totalAmount);
        
        // Redirect to success page
        window.location.href = `/booking_success/${bookingId}`;
        
    } catch (error) {
        modal.style.display = 'none';
        showError(document.body, error.message);
    }
}

// ===== REVIEWS FUNCTIONALITY =====

// Submit review
async function submitReview(movieId, customerName, rating, reviewText) {
    const reviewData = {
        movie_id: movieId,
        customer_name: customerName,
        rating: parseInt(rating),
        review_text: reviewText
    };
    
    try {
        const response = await fetch('/add_review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reviewData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showSuccess('Review submitted successfully!');
            setTimeout(() => location.reload(), 1000);
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        showError(document.body, 'Failed to submit review: ' + error.message);
    }
}

// ===== ADMIN FUNCTIONALITY =====

// Filter admin tables
function filterAdminTable(tableId, searchTerm, columnIndices) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const term = searchTerm.toLowerCase().trim();
    
    rows.forEach(row => {
        let shouldShow = false;
        
        columnIndices.forEach(index => {
            const cell = row.cells[index];
            if (cell && cell.textContent.toLowerCase().includes(term)) {
                shouldShow = true;
            }
        });
        
        row.style.display = shouldShow || !term ? '' : 'none';
    });
}

// Sort admin table
function sortAdminTable(tableId, columnIndex, dataType = 'string') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex]?.textContent?.trim() || '';
        const bValue = b.cells[columnIndex]?.textContent?.trim() || '';
        
        if (dataType === 'number') {
            return parseFloat(aValue) - parseFloat(bValue);
        } else if (dataType === 'date') {
            return new Date(aValue) - new Date(bValue);
        } else {
            return aValue.localeCompare(bValue);
        }
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// ===== MODAL MANAGEMENT =====

// Generic modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Reset form if exists
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
    }
}

// ===== FORM VALIDATION =====

// Validate email
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate phone number
function validatePhone(phone) {
    const phoneRegex = /^[+]?[\d\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone);
}

// Validate booking form
function validateBookingForm(formData) {
    const errors = [];
    
    if (!formData.get('customer_name')?.trim()) {
        errors.push('Name is required');
    }
    
    const email = formData.get('customer_email');
    if (!email?.trim()) {
        errors.push('Email is required');
    } else if (!validateEmail(email)) {
        errors.push('Please enter a valid email address');
    }
    
    const phone = formData.get('customer_phone');
    if (!phone?.trim()) {
        errors.push('Phone number is required');
    } else if (!validatePhone(phone)) {
        errors.push('Please enter a valid phone number');
    }
    
    if (selectedSeats.length === 0) {
        errors.push('Please select at least one seat');
    }
    
    return errors;
}

// ===== IMAGE HANDLING =====

// Handle image load errors
function handleImageError(img) {
    img.src = '/static/images/default-movie.jpg';
    img.alt = 'Movie poster not available';
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ===== ANALYTICS AND TRACKING =====

// Track user interactions
function trackEvent(eventName, data = {}) {
    // In a real application, this would send data to analytics service
    console.log('Event tracked:', eventName, data);
}

// Track page views
function trackPageView(pageName) {
    trackEvent('page_view', { page: pageName });
}

// Track booking steps
function trackBookingStep(step, data = {}) {
    trackEvent('booking_step', { step, ...data });
}

// ===== PERFORMANCE OPTIMIZATION =====

// Preload critical resources
function preloadCriticalResources() {
    const criticalResources = [
        '/static/css/style.css',
        '/static/js/main.js'
    ];
    
    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = resource;
        link.as = resource.endsWith('.css') ? 'style' : 'script';
        document.head.appendChild(link);
    });
}

// Cache API responses
const apiCache = new Map();

async function cachedFetch(url, options = {}) {
    const cacheKey = `${url}_${JSON.stringify(options)}`;
    
    if (apiCache.has(cacheKey)) {
        return apiCache.get(cacheKey);
    }
    
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        
        // Cache for 5 minutes
        setTimeout(() => apiCache.delete(cacheKey), 5 * 60 * 1000);
        
        apiCache.set(cacheKey, data);
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// ===== ACCESSIBILITY FEATURES =====

// Keyboard navigation for seat map
function handleSeatKeyNavigation(event) {
    const seat = event.target;
    if (!seat.classList.contains('seat') || seat.classList.contains('booked')) {
        return;
    }
    
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        seat.click();
    }
    
    // Arrow key navigation
    const allSeats = Array.from(document.querySelectorAll('.seat.available, .seat.selected'));
    const currentIndex = allSeats.indexOf(seat);
    let targetIndex = currentIndex;
    
    switch (event.key) {
        case 'ArrowLeft':
            targetIndex = Math.max(0, currentIndex - 1);
            break;
        case 'ArrowRight':
            targetIndex = Math.min(allSeats.length - 1, currentIndex + 1);
            break;
        case 'ArrowUp':
            targetIndex = Math.max(0, currentIndex - 10);
            break;
        case 'ArrowDown':
            targetIndex = Math.min(allSeats.length - 1, currentIndex + 10);
            break;
    }
    
    if (targetIndex !== currentIndex) {
        event.preventDefault();
        allSeats[targetIndex].focus();
    }
}

// ===== INITIALIZATION =====

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Track page view
    trackPageView(window.location.pathname);
    
    // Initialize lazy loading
    lazyLoadImages();
    
    // Preload critical resources
    preloadCriticalResources();
    
    // Add keyboard navigation to seat map
    const seatMap = document.getElementById('seatMap');
    if (seatMap) {
        seatMap.addEventListener('keydown', handleSeatKeyNavigation);
        
        // Make seats focusable
        setTimeout(() => {
            const seats = document.querySelectorAll('.seat.available');
            seats.forEach(seat => {
                seat.setAttribute('tabindex', '0');
            });
        }, 100);
    }
    
    // Initialize search functionality with debouncing
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        const targetTable = input.dataset.search;
        const searchFunction = debounce((term) => {
            // Implementation depends on specific table
            console.log('Searching in', targetTable, 'for', term);
        }, 300);
        
        input.addEventListener('input', (e) => searchFunction(e.target.value));
    });
    
    // Handle all modal close buttons
    document.querySelectorAll('.modal .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                closeModal(modal.id);
            }
        });
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    });
    
    // Handle image loading errors
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', () => handleImageError(img));
    });
    
    // Initialize payment method selection
    document.querySelectorAll('.payment-method').forEach(method => {
        method.addEventListener('click', function() {
            document.querySelectorAll('.payment-method').forEach(m => 
                m.classList.remove('selected')
            );
            this.classList.add('selected');
        });
    });
    
    console.log('MovieHub initialized successfully!');
});

// ===== ERROR HANDLING =====

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    // In production, send error to logging service
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    event.preventDefault();
});

// ===== EXPORT FOR TESTING =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatCurrency,
        validateEmail,
        validatePhone,
        validateBookingForm,
        filterMoviesByGenre,
        searchMovies
    };
}