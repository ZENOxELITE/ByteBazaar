# 🖥️ TechMart - Computer Parts E-commerce Platform

A modern, feature-rich e-commerce website built with Flask for selling computer parts and accessories. Features user authentication, shopping cart functionality, admin dashboard, and stunning RGB lighting effects in dark mode.

![TechMart](https://img.shields.io/badge/TechMart-E--commerce-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)

## ✨ Features

### 🛒 E-commerce Functionality
- **Product Catalog**: Browse 10+ categories of computer parts
- **Shopping Cart**: Add/remove items with quantity management
- **Checkout System**: Complete order processing with shipping details
- **Order History**: Track all past purchases
- **Search & Filter**: Find products by category, brand, or name
- **Product Details**: Comprehensive specifications and images

### 🔐 User Management
- **Replit Auth Integration**: Secure OAuth2 authentication
- **User Profiles**: Profile images and personal information
- **Admin Dashboard**: Product and order management
- **Role-based Access**: Admin-only features and pages

### 🎨 Modern UI/UX
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Dark/Light Themes**: Toggle with localStorage persistence
- **RGB Lightning Effects**: Animated hover effects in dark mode
- **Animated Homepage**: Computer illustration with floating icons
- **Interactive Elements**: Smooth transitions and hover effects

### ⚡ Technical Features
- **Flask Backend**: Python web framework with SQLAlchemy ORM
- **PostgreSQL Database**: Robust relational database
- **Session Management**: Secure user sessions with Flask-Login
- **Custom CSS Animations**: RGB effects and smooth transitions
- **Production Ready**: Gunicorn WSGI server configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd techmart
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if using `uv`:
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost/techmart
   SESSION_SECRET=your-secure-session-secret-key
   REPL_ID=your-replit-id  # For Replit Auth
   ISSUER_URL=https://replit.com/oidc  # Optional, defaults to this
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Run the application**
   ```bash
   # Development mode
   python main.py
   
   # Production mode with Gunicorn
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🗄️ Database Setup

### PostgreSQL to MySQL Migration

If you want to use MySQL instead of PostgreSQL (for XAMPP setup):

1. **Install MySQL dependencies**
   ```bash
   pip install pymysql
   ```

2. **Update database URL in `.env`**
   ```env
   DATABASE_URL=mysql+pymysql://username:password@localhost/techmart
   ```

3. **Create MySQL database**
   ```sql
   CREATE DATABASE techmart;
   ```

4. **Run the application** - tables will be created automatically

### Sample Data

The application comes with pre-populated sample data including:
- 10 product categories (CPUs, GPUs, RAM, Storage, etc.)
- 16+ sample products with real specifications
- Category icons and descriptions

## 📁 Project Structure

```
techmart/
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles with RGB effects
│   └── js/
│       └── main.js            # Theme toggle and interactions
├── templates/
│   ├── admin/                 # Admin dashboard templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Homepage with animations
│   ├── products.html          # Product catalog
│   ├── cart.html              # Shopping cart
│   └── ...                    # Other page templates
├── app.py                     # Flask application setup
├── main.py                    # Application entry point
├── models.py                  # Database models
├── routes.py                  # URL routes and views
├── replit_auth.py             # Authentication blueprint
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎨 Theme System

### Dark Mode Features
- **Automatic Theme Switching**: Toggle button in navigation
- **RGB Lightning Effects**: Hover animations on cards
- **Persistent Preferences**: Uses localStorage
- **Enhanced Visuals**: Glowing borders and electric effects

### Customization
Modify `static/css/style.css` to customize:
- RGB color schemes
- Animation speeds
- Hover effects
- Theme variables

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | Yes | - |
| `SESSION_SECRET` | Flask session secret key | Yes | - |
| `REPL_ID` | Replit application ID | For auth | - |
| `ISSUER_URL` | OAuth issuer URL | No | `https://replit.com/oidc` |

### Admin Setup
To make a user an admin:
```sql
UPDATE users SET is_admin = true WHERE email = 'admin@example.com';
```

## 🛠️ Development

### Running in Development Mode
```bash
# With debug mode enabled
export FLASK_ENV=development
python main.py
```

### Database Migrations
```bash
# Create new tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Drop all tables (caution!)
python -c "from app import app, db; app.app_context().push(); db.drop_all()"
```

### Adding New Products
1. Access admin dashboard at `/admin/dashboard`
2. Click "Add New Product"
3. Fill in product details and specifications
4. Upload product image or use URL

## 🚀 Deployment

### Replit Deployment
1. Connect your Replit to the repository
2. Set environment variables in Secrets
3. Run the application using the configured workflow

### Traditional Hosting
1. Install dependencies on server
2. Set up PostgreSQL/MySQL database
3. Configure environment variables
4. Use Gunicorn with systemd service
5. Set up reverse proxy with Nginx

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Product browsing and search
- [ ] Add/remove items from cart
- [ ] Checkout process
- [ ] Order history viewing
- [ ] Admin product management
- [ ] Theme switching functionality
- [ ] RGB effects in dark mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Database Connection Error**
- Check DATABASE_URL format
- Ensure database server is running
- Verify credentials

**Authentication Issues**
- Check REPL_ID configuration
- Verify SESSION_SECRET is set
- Ensure OAuth redirect URLs are correct

**Theme Not Switching**
- Clear browser cache
- Check JavaScript console for errors
- Verify theme files are loaded

### Getting Help
- Check the documentation in `replit.md`
- Review error logs in the browser console
- Ensure all environment variables are set correctly

## 🎯 Roadmap

- [ ] Payment integration (Stripe/PayPal)
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Inventory management
- [ ] Mobile app development

---

**Built with ❤️ using Flask, Bootstrap, and modern web technologies**