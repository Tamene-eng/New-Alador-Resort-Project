import logging
from dotenv import load_dotenv
from app import create_app

# Load environment variables early
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.INFO)

# Create Flask app (basic version)
app = create_app()

# Run the app
if __name__ == "__main__":
    logging.info("🚀 Starting Flask app")
    app.run(debug=True, host="127.0.0.1", port=5000)
