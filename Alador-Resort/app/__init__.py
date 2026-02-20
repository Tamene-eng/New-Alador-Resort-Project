import os
import sqlite3
import logging
import base64
import io
import json
import uuid
import requests
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, url_for, flash, session,
    send_file, send_from_directory, Response, g
)
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- Logging Setup ---
logging.basicConfig(filename='logs/error.log', level=logging.ERROR)
logger = logging.getLogger(__name__)

# --- Config Loader ---
def load_config(path="config.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        return json.load(f)

def get_env_variable(key, default=None):
    value = os.getenv(key)
    if value is None:
        logger.warning(f"⚠️ Missing {key}. Using default: {default}")
        return default
    return value

# --- App Factory ---
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(load_config())

    app.secret_key = app.config.get("SECRET_KEY", "dev_secret_key")

    # --- Flask-Login Setup ---
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    # --- User Model ---
    class User(UserMixin):
        def __init__(self, id, username, password, role="user"):
            self.id = id
            self.username = username
            self.password = password
            self.role = role

    @login_manager.user_loader
    def load_user(user_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role FROM users WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            return User(*data) if data else None

    # --- CLI Command Example ---
    @app.cli.command("create-admin")
    def create_admin():
        admin = User(str(uuid.uuid4()), "admin", generate_password_hash("admin123"), "admin")
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
                (admin.id, admin.username, admin.password, admin.role)
            )
            conn.commit()
        click.echo("✅ Admin user created.")

    # --- Database Helpers ---
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect("database.db")
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    # --- Routes ---
    @app.route('/')
    def index():
        weather = get_weather("Addis Ababa")
        return render_template("index.html", weather=weather)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form["username"]
            password = generate_password_hash(request.form["password"])
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                db.commit()
                flash("Account created successfully! You may now log in.", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Username already exists. Choose a different one.", "warning")
        return render_template("register.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            user_data = db.execute(
                "SELECT id, username, password, role FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if user_data and check_password_hash(user_data[2], password):
                user = User(*user_data)
                login_user(user)
                flash("Welcome back!", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials. Please try again.", "danger")
        return render_template("login.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        db = get_db()
        bookings = db.execute(
            "SELECT id, date, activity, status FROM bookings WHERE user_id = ?",
            (current_user.id,)
        ).fetchall()
        return render_template("dashboard.html", bookings=bookings)

    @app.route('/book', methods=['POST'])
    @login_required
    def book():
        date = request.form["date"]
        activity = request.form["activity"]
        reservation_id = str(uuid.uuid4())[:8]
        db = get_db()
        db.execute(
            "INSERT INTO bookings (reservation_id, user_id, date, activity, status) VALUES (?, ?, ?, ?, 'pending')",
            (reservation_id, current_user.id, date, activity)
        )
        db.commit()
        flash("✅ Your booking was submitted!", "success")
        return redirect(url_for("dashboard"))

    # --- Utility: Weather ---
    def get_weather(city="Addis Ababa"):
        api_key = app.config.get("WEATHER_API_KEY")
        if not api_key:
            return {"error": "Missing API key"}
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = resp.json()
            return {
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"]
            }
        except Exception as e:
            logger.error(f"Weather fetch error: {e}")
            return {"error": "Could not fetch weather"}

    # --- Error Handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server Error: {e}")
        return render_template("500.html"), 500

    # --- Context Processor ---
    @app.context_processor
    def inject_year():
        return {"current_year": datetime.now().year}

    # --- Add more routes as needed! ---

    return app

# --- Entry Point ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)