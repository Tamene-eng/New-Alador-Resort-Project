import os


def get_env_variable(var_name, default=""):
    """Retrieves an environment variable or
    returns the 'default' string if the variable is not set. """
    value = os.environ.get(var_name)
    if value is None:
        return str(default)
    return str(value)


def validate_env_keys(required_keys):
    """Checks if all required environment variables are present."""
    missing = [key for key in required_keys if key not in os.environ]
    if missing:
        print(f"Warning: Missing environment variables: {', '.join(missing)}")
    return not bool(missing)


class Config:
    """Base configuration class."""
    DEBUG = True
    SECRET_KEY = "dev-secret-key"
    # Add other settings here as needed


def get_config(env_name=None):
    """
    Returns the Config CLASS itself, not an instance.
    This fixes the 'dict' object has no attribute 'name' error.
    """
    return Config


import click
from flask.cli import with_appcontext


def register_cli(app):
    """
    This function attaches custom CLI commands to your Flask app.
    It matches the 'register_cli(app)' call in your run.py.
    """

    @app.cli.command("init-db")
    @with_appcontext
    def init_db_command():
        """Clear existing data and create new tables."""
        # Add your database initialization logic here
        click.echo("Initialized the database.")

    @app.cli.command("hello")
    def hello_command():
        """A simple test command."""
        click.echo("Hello from the custom CLI!")

    # You can add more @app.cli.command functions here


