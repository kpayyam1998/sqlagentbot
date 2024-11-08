import os
import logging
from datetime import datetime
from flask import Flask
from logging.config import dictConfig

from logging.handlers import RotatingFileHandler

if not os.path.exists("logs"):
    os.makedirs("logs")

#Log file_name
log_file_name = f"logs/app_logs{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"


# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'console': {                                  # Console output for real-time viewing
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'file': {                                     # Rotating file handler for persistent logs
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_name,
            'maxBytes': 1000000,                      # 1 MB file size before rotation
            'backupCount': 5,                         # Keep up to 5 old log files
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',                              # Set global log level
        'handlers': ['console', 'file']               # Use both console and file handlers
    }
})

# Create a Flask application
app = Flask(__name__)

# Define a simple route
@app.route('/')
def home():
    app.logger.info("Home route accessed.")          # Logs INFO level message
    return "Welcome to the real-time Flask app!"

# Another route to test error logging
@app.route('/error')
def error():
    app.logger.error("An error occurred!")           # Logs ERROR level message
    return "An error occurred", 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
