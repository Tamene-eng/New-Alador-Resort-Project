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