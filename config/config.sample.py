# Statement for enabling the development environment
DEBUG = False

# Define the application directory
import os
CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
BUGZILLA_DATABASE_URI = ''
SETTINGS_DATABASE_URI = ''

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

SERVER_NAME = '127.0.0.1:9003'
