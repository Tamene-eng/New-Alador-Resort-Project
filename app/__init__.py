import sqlite3
from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# Initialize extensions
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "main.login"  # Note the 'main.' prefix


def create_app():
    app = Flask(__name__)

    # Simple Config (You can keep your Config class too)
    app.secret_key = "dev_secret_key"
    app.config["WEATHER_API_KEY"] = "your_key_here"

    # Connect Extensions
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Register the routes from routes.py
    from .routes import main, User
    app.register_blueprint(main)

    # User Loader (Needs to be here to link login_manager to the User class)
    @login_manager.user_loader
    def load_user(user_id):
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            if data:
                return User(data['id'], data['username'], data['password'], data['role'])
            return None

    # Database cleanup
    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()
    @app.context_processor
    def inject_brand():
        return {
            "brand": {"resort_name": "Alador Resort"}
        }

    return app