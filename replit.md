# TechMart - Computer Parts E-commerce Platform

## Overview

TechMart is a Flask-based e-commerce platform specializing in computer parts and accessories. The application provides a comprehensive online shopping experience with user authentication, product catalog management, shopping cart functionality, and order processing. It features a complete admin panel for managing products, categories, and orders, with integration to Replit's authentication system for seamless user login.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask Application**: Built using Flask with SQLAlchemy ORM for database operations
- **Database Models**: Comprehensive schema including Users, Products, Categories, Cart Items, Orders, and OAuth tokens
- **Authentication**: Integrated with Replit Auth using OAuth2 flow with Flask-Dance for social login
- **Session Management**: Flask-Login for user session handling with permanent sessions

### Database Design
- **User System**: User model with profile information, admin flags, and relationship mappings
- **Product Catalog**: Products with categories, pricing, stock management, and metadata (brand, model, specifications)
- **Shopping Cart**: Persistent cart items linked to users with quantity tracking
- **Order Management**: Complete order workflow with order items, shipping details, and status tracking
- **OAuth Storage**: Custom storage implementation for managing OAuth tokens per user session

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 for responsive design
- **Component Structure**: Modular template inheritance with base layout and specialized pages
- **User Interface**: Modern responsive design with Font Awesome icons and custom CSS
- **Client-side Functionality**: JavaScript for enhanced UX including form animations, alert management, and theme switching
- **Theme System**: Dark/Light mode toggle with RGB lighting effects in dark mode and localStorage persistence
- **Visual Effects**: Animated computer illustration on homepage with floating tech icons and smooth transitions

### Authentication & Authorization
- **Replit Auth Integration**: OAuth2 flow with browser session key tracking
- **Role-based Access**: Admin users have access to management interfaces
- **Session Security**: Secure session management with proper logout and token cleanup

### Application Structure
- **Route Organization**: Separated route definitions with dedicated admin routes
- **Error Handling**: Custom error pages (403) with proper user feedback
- **Static Assets**: CSS and JavaScript files for styling and client-side functionality
- **Template Hierarchy**: Organized template structure with admin-specific templates

## External Dependencies

### Authentication Services
- **Replit Auth**: Primary authentication provider using OAuth2 protocol
- **Flask-Dance**: OAuth client library for handling authentication flows

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for consistent iconography
- **jQuery/Bootstrap JS**: Client-side functionality for interactive components

### Python Packages
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: Database ORM and management
- **Flask-Login**: User session management
- **Werkzeug**: WSGI utilities including proxy fix for HTTPS
- **PyJWT**: JSON Web Token handling for authentication

### Database
- **SQLAlchemy**: ORM with support for multiple database backends
- **Connection Pooling**: Configured for production use with connection recycling and health checks

### Development Tools
- **Environment Variables**: Configuration through environment variables for database URL and session secrets
- **Logging**: Debug-level logging configured for development and troubleshooting