import uuid
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import current_user
from sqlalchemy import or_
from app import app, db
from replit_auth import require_login, make_replit_blueprint
from models import User, Category, Product, CartItem, Order, OrderItem

app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home')
@require_login
def home():
    # Get featured products and categories
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    categories = Category.query.all()
    
    # Get cart count
    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('home.html', 
                         featured_products=featured_products, 
                         categories=categories,
                         cart_count=cart_count)

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(or_(
            Product.name.contains(search),
            Product.description.contains(search),
            Product.brand.contains(search)
        ))
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.name.asc())
    
    products_pagination = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.all()
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('products.html', 
                         products=products_pagination.items,
                         pagination=products_pagination,
                         categories=categories,
                         current_category=category_id,
                         current_search=search,
                         current_sort=sort_by,
                         cart_count=cart_count)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related_products,
                         cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@require_login
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if not product.in_stock or product.stock_quantity < quantity:
        flash('Product is out of stock or insufficient quantity available.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem()
        cart_item.user_id = current_user.id
        cart_item.product_id = product_id
        cart_item.quantity = quantity
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
@require_login
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.total_price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@require_login
def update_cart(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@require_login
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
@require_login
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    
    total = sum(item.total_price for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
@require_login
def place_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    
    # Get form data
    shipping_address = request.form.get('shipping_address')
    phone_number = request.form.get('phone_number')
    notes = request.form.get('notes', '')
    
    if not shipping_address or not phone_number:
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('checkout'))
    
    # Create order
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    total_amount = sum(item.total_price for item in cart_items)
    
    order = Order()
    order.order_number = order_number
    order.user_id = current_user.id
    order.total_amount = total_amount
    order.shipping_address = shipping_address
    order.phone_number = phone_number
    order.notes = notes
    db.session.add(order)
    db.session.flush()  # Get the order ID
    
    # Create order items and update stock
    for cart_item in cart_items:
        order_item = OrderItem()
        order_item.order_id = order.id
        order_item.product_id = cart_item.product_id
        order_item.quantity = cart_item.quantity
        order_item.price = cart_item.product.price
        db.session.add(order_item)
        
        # Update product stock
        cart_item.product.stock_quantity -= cart_item.quantity
    
    # Clear cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    flash(f'Order {order_number} placed successfully!', 'success')
    return redirect(url_for('orders'))

@app.route('/orders')
@require_login
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return render_template('orders.html', orders=user_orders, cart_count=cart_count)

# Admin routes
@app.route('/admin')
@require_login
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Admin dashboard statistics
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         pending_orders=pending_orders)

@app.route('/admin/products')
@require_login
def admin_products():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    page = request.args.get('page', 1, type=int)
    products_pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/products.html', products=products_pagination.items, pagination=products_pagination)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@require_login
def admin_add_product():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        product = Product()
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price') or 0)
        product.stock_quantity = int(request.form.get('stock_quantity') or 0)
        product.image_url = request.form.get('image_url')
        product.brand = request.form.get('brand')
        product.model = request.form.get('model')
        product.specifications = request.form.get('specifications')
        product.category_id = int(request.form.get('category_id') or 1)
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

# Initialize categories if they don't exist
def create_default_categories():
    if Category.query.count() == 0:
        categories = [
            {'name': 'Processors (CPUs)', 'description': 'Intel and AMD processors', 'icon': 'fas fa-microchip'},
            {'name': 'Graphics Cards (GPUs)', 'description': 'NVIDIA and AMD graphics cards', 'icon': 'fas fa-tv'},
            {'name': 'Memory (RAM)', 'description': 'DDR4 and DDR5 memory modules', 'icon': 'fas fa-memory'},
            {'name': 'Storage', 'description': 'SSDs and HDDs', 'icon': 'fas fa-hdd'},
            {'name': 'Motherboards', 'description': 'ATX, Micro-ATX, and Mini-ITX motherboards', 'icon': 'fas fa-server'},
            {'name': 'Power Supplies', 'description': 'Modular and non-modular PSUs', 'icon': 'fas fa-plug'},
            {'name': 'Cases', 'description': 'Full tower, mid tower, and mini cases', 'icon': 'fas fa-desktop'},
            {'name': 'Cooling', 'description': 'Air and liquid cooling solutions', 'icon': 'fas fa-fan'},
            {'name': 'Peripherals', 'description': 'Keyboards, mice, and monitors', 'icon': 'fas fa-keyboard'},
            {'name': 'Accessories', 'description': 'Cables, adapters, and other accessories', 'icon': 'fas fa-tools'}
        ]
        
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()

# Create default categories when app starts
with app.app_context():
    create_default_categories()
