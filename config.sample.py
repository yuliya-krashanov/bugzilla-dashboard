import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
BUGZILLA_DATABASE_URI = ''
SETTINGS_DATABASE_URI = ''

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = ""

# Secret key for signing cookies
SECRET_KEY = ""
