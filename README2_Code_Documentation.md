# 📖 TechMart - Complete Code Documentation

This document provides detailed explanations of every component, function, and logic in the TechMart e-commerce application.

## 📁 Project Structure Overview

```
techmart/
├── static/                    # Static assets (CSS, JS, images)
├── templates/                 # HTML templates
├── app.py                    # Flask application setup
├── main.py                   # Application entry point
├── models.py                 # Database models
├── routes.py                 # URL routes and business logic
├── replit_auth.py            # Authentication system
└── requirements files        # Dependencies
```

---

## 🔧 Core Application Files

### app.py - Flask Application Setup

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
```

**What this does:**
- Creates the main Flask application instance
- Sets up logging for development debugging
- Configures session secret from environment variables
- Adds ProxyFix middleware for HTTPS URL generation
- Creates SQLAlchemy base class for database models

**Database Configuration:**
```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
}
```

**What this does:**
- Connects to PostgreSQL database via environment variable
- Disables modification tracking for better performance
- Enables connection health checks (pool_pre_ping)
- Recycles connections every 300 seconds to prevent timeouts

### main.py - Application Entry Point

```python
from app import app
import routes  # noqa: F401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

**What this does:**
- Imports the Flask app from app.py
- Imports routes to register URL endpoints
- Starts development server on all interfaces (0.0.0.0) port 5000
- Enables debug mode for auto-reload and error details

---

## 🗄️ Database Models (models.py)

### User Model
```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
```

**What this does:**
- Inherits from UserMixin for Flask-Login integration
- Uses String ID to work with Replit Auth (user IDs are strings)
- Stores user profile information from OAuth
- Includes admin flag for role-based access control
- Links to orders and cart items via relationships

### Product Model
```python
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    specifications = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
```

**What this does:**
- Stores product information with precise decimal pricing
- Links to categories via foreign key relationship
- Includes inventory tracking with stock_quantity
- Stores product images as URLs (works with CDNs)
- Supports detailed specifications in HTML format
- Tracks creation and modification timestamps

### Category Model
```python
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    products = db.relationship('Product', backref='category', lazy=True)
```

**What this does:**
- Organizes products into categories (CPUs, GPUs, etc.)
- Uses Font Awesome icon classes for visual representation
- Creates bidirectional relationship with products
- Ensures unique category names to prevent duplicates

### Shopping Cart Model
```python
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
```

**What this does:**
- Stores user's shopping cart items persistently
- Links users to products with specified quantities
- Prevents data loss when users close browser
- Enables cart calculations and checkout process

### Order System Models
```python
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
```

**What this does:**
- Creates complete order tracking system
- Stores historical pricing in OrderItem (prevents price changes affecting old orders)
- Tracks order status (pending, processing, shipped, delivered)
- Maintains shipping information for fulfillment

---

## 🔐 Authentication System (replit_auth.py)

### OAuth Configuration
```python
def make_replit_blueprint():
    try:
        repl_id = os.environ['REPL_ID']
    except KeyError:
        raise SystemExit("the REPL_ID environment variable must be set")

    replit_bp = OAuth2ConsumerBlueprint(
        "replit_auth",
        __name__,
        client_id=repl_id,
        client_secret=None,
        base_url=issuer_url,
        authorization_url=issuer_url + "/auth",
        token_url=issuer_url + "/token",
        scope=["openid", "profile", "email", "offline_access"],
    )
```

**What this does:**
- Creates OAuth2 client for Replit authentication
- Uses REPL_ID as the OAuth client ID
- Requests OpenID, profile, email, and offline access scopes
- No client secret needed (public client with PKCE)

### Session Management
```python
class UserSessionStorage(BaseStorage):
    def get(self, blueprint):
        try:
            token = db.session.query(OAuth).filter_by(
                user_id=current_user.get_id(),
                browser_session_key=g.browser_session_key,
                provider=blueprint.name,
            ).one().token
        except NoResultFound:
            token = None
        return token
```

**What this does:**
- Stores OAuth tokens in database instead of memory
- Links tokens to specific browser sessions
- Supports multiple concurrent sessions per user
- Prevents token conflicts between browser tabs

### User Creation Logic
```python
def save_user(user_claims):
    user = User()
    user.id = user_claims['sub']
    user.email = user_claims.get('email')
    user.first_name = user_claims.get('first_name')
    user.last_name = user_claims.get('last_name')
    user.profile_image_url = user_claims.get('profile_image_url')
    merged_user = db.session.merge(user)
    db.session.commit()
    return merged_user
```

**What this does:**
- Extracts user information from OAuth ID token
- Creates or updates user record in database
- Uses merge() to handle both new and existing users
- Returns user object for Flask-Login session

---

## 🛣️ URL Routes and Business Logic (routes.py)

### Homepage Route
```python
@app.route('/')
def index():
    categories = Category.query.limit(4).all()
    return render_template('index.html', categories=categories)
```

**What this does:**
- Displays landing page with featured categories
- Limits categories to 4 for homepage preview
- Renders index.html template with category data

### Product Catalog Route
```python
@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    query = Product.query.filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.paginate(
        page=page, per_page=12, error_out=False
    )
```

**What this does:**
- Implements product browsing with pagination
- Supports category filtering via URL parameter
- Enables product search by name
- Returns 12 products per page
- Handles invalid page numbers gracefully

### Shopping Cart Logic
```python
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@require_login
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    existing_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
```

**What this does:**
- Requires user authentication to add items
- Validates product exists (404 if not found)
- Updates quantity if item already in cart
- Creates new cart item if not exists
- Commits changes to database

### Checkout Process
```python
@app.route('/checkout', methods=['GET', 'POST'])
@require_login
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=request.form['shipping_address']
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
```

**What this does:**
- Validates cart is not empty before checkout
- Creates order record with total amount
- Copies cart items to order items with current prices
- Clears user's cart after successful order
- Uses database transaction to ensure data consistency

### Admin Dashboard Routes
```python
@app.route('/admin/dashboard')
@require_login
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
```

**What this does:**
- Restricts access to admin users only
- Calculates key business metrics
- Shows recent orders for quick overview
- Returns 403 Forbidden for non-admin users

---

## 🎨 Frontend Templates

### Base Template (templates/base.html)
```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TechMart{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
```

**What this does:**
- Provides consistent layout for all pages
- Includes Bootstrap 5 for responsive design
- Loads Font Awesome icons for UI elements
- Sets up theme system with data-theme attribute
- Uses block templates for page-specific content

### Navigation Bar
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('index') }}">
            <i class="fas fa-laptop me-2"></i>TechMart
        </a>
        
        <div class="navbar-nav ms-auto">
            <li class="nav-item">
                <button class="btn btn-outline-light btn-sm me-2" id="theme-toggle" onclick="toggleTheme()">
                    <i class="fas fa-moon" id="theme-icon"></i>
                </button>
            </li>
        </div>
    </div>
</nav>
```

**What this does:**
- Creates responsive navigation bar
- Shows brand logo and name
- Includes theme toggle button
- Displays user authentication status
- Shows cart item count for logged-in users

### Product Display Template
```html
<div class="col-lg-3 col-md-6 mb-4">
    <div class="card product-card h-100">
        <div class="product-image">
            <img src="{{ product.image_url }}" class="card-img-top" alt="{{ product.name }}">
        </div>
        <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text text-muted">{{ product.brand }} {{ product.model }}</p>
            <p class="price fw-bold">${{ "%.2f"|format(product.price) }}</p>
        </div>
    </div>
</div>
```

**What this does:**
- Creates responsive product grid layout
- Displays product image, name, and price
- Uses Bootstrap classes for consistent styling
- Formats price to 2 decimal places
- Links to detailed product pages

---

## 🎨 Styling System (static/css/style.css)

### CSS Variables and Theme System
```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    --info-color: #0dcaf0;
    --light-color: #f8f9fa;
    --dark-color: #212529;
}

[data-theme="dark"] {
    --bg-color: #121212;
    --surface-color: #1e1e1e;
    --text-color: #ffffff;
    --text-muted: #aaaaaa;
    --border-color: #333;
}
```

**What this does:**
- Defines consistent color scheme across application
- Enables theme switching with CSS custom properties
- Provides light and dark theme variables
- Ensures accessibility with proper contrast ratios

### RGB Lightning Effects
```css
[data-theme="dark"] .category-card::before {
    content: '';
    position: absolute;
    background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b, #ff4757, #ff006e);
    background-size: 400% 400%;
    animation: rgbLightning 2s ease-in-out infinite;
    opacity: 0;
    transition: all 0.3s ease;
    filter: blur(8px);
}

[data-theme="dark"] .category-card:hover::before {
    opacity: 1;
    filter: blur(12px);
    animation: rgbLightning 1s ease-in-out infinite, electricPulse 0.5s ease-in-out infinite;
}
```

**What this does:**
- Creates animated rainbow borders around cards
- Uses CSS pseudo-elements for layered effects
- Activates on hover with increased intensity
- Combines multiple animations for dynamic appearance
- Only visible in dark mode for dramatic effect

### Responsive Design
```css
@media (max-width: 768px) {
    .hero-icon {
        font-size: 4rem;
    }
    
    .category-card {
        padding: 1rem;
    }
    
    .product-image {
        height: 180px;
    }
}
```

**What this does:**
- Adapts layout for mobile devices
- Reduces icon sizes on small screens
- Adjusts card padding for touch interfaces
- Optimizes image dimensions for mobile viewing

---

## ⚙️ JavaScript Functionality (static/js/main.js)

### Theme Toggle System
```javascript
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    const themeIcon = document.getElementById('theme-icon');
    if (newTheme === 'dark') {
        themeIcon.className = 'fas fa-sun';
    } else {
        themeIcon.className = 'fas fa-moon';
    }
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        if (savedTheme === 'dark') {
            themeIcon.className = 'fas fa-sun';
        } else {
            themeIcon.className = 'fas fa-moon';
        }
    }
}
```

**What this does:**
- Toggles between light and dark themes
- Saves user preference in browser localStorage
- Updates theme icon (moon for light mode, sun for dark mode)
- Applies theme immediately without page reload
- Restores saved theme on page load

### Interactive Elements
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
```

**What this does:**
- Initializes all interactive components on page load
- Sets up Bootstrap tooltips for help text
- Auto-hides flash messages after 5 seconds
- Ensures theme is applied before page renders

---

## 📦 How to Add New Products

### Method 1: Admin Dashboard (Recommended)
1. **Login as Admin:**
   - Set user as admin: `UPDATE users SET is_admin = true WHERE email = 'your@email.com';`
   - Access admin dashboard at `/admin/dashboard`

2. **Add Product Form:**
   - Click "Add New Product" button
   - Fill in required fields:
     - **Name**: Product display name
     - **Description**: Detailed product description
     - **Price**: Decimal price (e.g., 199.99)
     - **Stock Quantity**: Available inventory
     - **Category**: Select from dropdown
     - **Brand**: Manufacturer name
     - **Model**: Product model number
     - **Specifications**: HTML-formatted specs
     - **Image URL**: Product image link

3. **Save Product:**
   - Click "Add Product" button
   - Product appears immediately in catalog

### Method 2: Direct Database Insert
```sql
INSERT INTO products (
    name, description, price, stock_quantity, 
    image_url, brand, model, specifications, 
    category_id, is_active, created_at, updated_at
) VALUES (
    'AMD Ryzen 5 7600X',
    'High-performance 6-core gaming processor',
    229.99,
    50,
    'https://example.com/ryzen5.jpg',
    'AMD',
    'Ryzen 5 7600X',
    '• 6 cores, 12 threads<br>• Base Clock: 4.7 GHz<br>• Max Boost: 5.3 GHz',
    1,
    true,
    NOW(),
    NOW()
);
```

### Method 3: Python Script
```python
from app import app, db
from models import Product, Category

with app.app_context():
    # Find category
    cpu_category = Category.query.filter_by(name='Processors (CPUs)').first()
    
    # Create product
    new_product = Product(
        name='Intel Core i5-13600K',
        description='Mid-range gaming processor with excellent performance',
        price=289.99,
        stock_quantity=30,
        brand='Intel',
        model='i5-13600K',
        specifications='• 14 cores (6P + 8E)<br>• Base Clock: 3.5 GHz<br>• Max Boost: 5.1 GHz',
        category_id=cpu_category.id,
        is_active=True
    )
    
    db.session.add(new_product)
    db.session.commit()
    print(f"Added product: {new_product.name}")
```

---

## 🔧 How to Add New Categories

### Method 1: Direct Database Insert
```sql
INSERT INTO categories (name, description, icon, created_at) VALUES 
('Laptops', 'Gaming and professional laptops', 'fas fa-laptop', NOW()),
('Monitors', 'LCD, OLED, and gaming monitors', 'fas fa-desktop', NOW()),
('Audio', 'Headphones, speakers, and sound cards', 'fas fa-headphones', NOW());
```

### Method 2: Python Script
```python
from app import app, db
from models import Category

with app.app_context():
    categories = [
        {
            'name': 'Network Equipment',
            'description': 'Routers, switches, and network cards',
            'icon': 'fas fa-wifi'
        },
        {
            'name': 'Software',
            'description': 'Operating systems and applications',
            'icon': 'fas fa-code'
        }
    ]
    
    for cat_data in categories:
        category = Category(**cat_data)
        db.session.add(category)
    
    db.session.commit()
    print("Categories added successfully!")
```

---

## 🎯 Common Customizations

### Adding New User Fields
1. **Update User Model:**
```python
class User(UserMixin, db.Model):
    # Existing fields...
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
```

2. **Update Templates:**
```html
<div class="mb-3">
    <label for="phone" class="form-label">Phone Number</label>
    <input type="tel" class="form-control" id="phone" name="phone_number" value="{{ current_user.phone_number }}">
</div>
```

### Adding Product Reviews
1. **Create Review Model:**
```python
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
```

2. **Add Review Route:**
```python
@app.route('/product/<int:product_id>/review', methods=['POST'])
@require_login
def add_review(product_id):
    rating = int(request.form['rating'])
    comment = request.form['comment']
    
    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('product_detail', id=product_id))
```

### Customizing Email Notifications
1. **Install Flask-Mail:**
```bash
pip install Flask-Mail
```

2. **Configure Email:**
```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

def send_order_confirmation(order):
    msg = Message(
        'Order Confirmation - TechMart',
        sender=app.config['MAIL_USERNAME'],
        recipients=[order.user.email]
    )
    msg.body = f'Your order #{order.id} has been confirmed!'
    mail.send(msg)
```

---

## 🐛 Troubleshooting Common Issues

### Database Connection Errors
```python
# Check database URL format
print(os.environ.get('DATABASE_URL'))

# Test connection
from app import db
try:
    db.session.execute('SELECT 1')
    print("Database connected successfully!")
except Exception as e:
    print(f"Database error: {e}")
```

### Theme Not Switching
1. **Check JavaScript Console:** Open browser dev tools for errors
2. **Verify CSS Loading:** Ensure style.css loads without 404 errors
3. **Clear Browser Cache:** Hard refresh with Ctrl+F5

### OAuth Authentication Issues
1. **Check Environment Variables:**
```bash
echo $REPL_ID
echo $SESSION_SECRET
```

2. **Verify Redirect URLs:** Ensure OAuth app settings match your domain

### Performance Optimization
1. **Add Database Indexes:**
```sql
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_cart_user ON cart_items(user_id);
```

2. **Enable Query Caching:**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
```

This comprehensive documentation covers every aspect of the TechMart application, from basic setup to advanced customizations. Use this as your reference guide for understanding, maintaining, and extending the codebase.