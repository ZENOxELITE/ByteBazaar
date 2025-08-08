# routes.py
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from sqlalchemy import or_
from flask_dance.contrib.google import google
from models import User, Category, Product, CartItem, Order, OrderItem
from app import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/shop")
def shop():
    products = Product.query.all()
    return render_template("shop.html", products=products)

@main.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)

@main.route("/category/<int:category_id>")
def category(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("category.html", category=category, products=products)

@main.route("/cart")
def cart():
    cart_items = CartItem.query.all()
    return render_template("cart.html", cart_items=cart_items)

@main.route("/checkout")
def checkout():
    return render_template("checkout.html")

@main.route("/login/google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()
    return f"Logged in as {user_info['email']}"

@main.route("/search")
def search():
    query = request.args.get("q", "")
    results = Product.query.filter(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
    ).all()
    return render_template("search.html", query=query, results=results)
