import sqlite3
import uuid
import requests
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Blueprint
main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


# --- User Model ---
class User(UserMixin):
    def __init__(self, user_id, username, password, role="user"):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role


# --- Database Helpers ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row  # Allows accessing data by name: user['username']
    return g.db


def get_weather(city="Addis Ababa"):
    api_key = "d76306fd6f5956fce6d476463f022e68"
    url = f"https://openweathermap.org{city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") == 200:
            # Re-structure the data to match your index.html exactly
            return {
                "main": {"temp": round(data["main"]["temp"])},
                "weather": {
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                },
                "name": data["name"]
            }
        else:
            print(f"API error: {data.get('message')}")

    except Exception as e:
        print(f"Connection Error: {e}")

    return {"error": "Weather data unavailable."}


# --- ALL ROUTES GO HERE ---

@main.route('/')
def index():
    weather = get_weather()
    styles = {"main": "css/styles.css"}
    return render_template("index.html", weather=weather, styles=styles)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            db = get_db()
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for("main.login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "warning")
    return render_template("register.html")


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user_data = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], user_data['username'], user_data['password'], user_data['role'])
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("login.html")


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))


@main.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    bookings = db.execute("SELECT * FROM bookings WHERE user_id = ?", (current_user.id,)).fetchall()
    return render_template("dashboard.html", bookings=bookings)


@main.route('/book', methods=['POST'])
def book():
    date = request.form["date"]
    activity = request.form["activity"]
    res_id = str(uuid.uuid4())[:8]
    db = get_db()
    db.execute("INSERT INTO bookings (reservation_id, user_id, date, activity, status) VALUES (?, ?, ?, ?, 'pending')",
               (res_id, current_user.id, date, activity))
    db.commit()
    flash("✅ Booking submitted!", "success")
    return redirect(url_for("dashboard.html"))


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/contact')
def contact():
    return render_template("contact.html")


@main.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    return render_template("main.admin_dashboard")


@main.route('/weather_preview')
def weather_preview_route():
    return render_template("weather_preview.html")


@main.route('/qr_preview')
def qr_preview_route():
    return render_template("qr_preview.html")

@main.route('/gallery')
def gallery():
    return "Gallery Coming Soon"

