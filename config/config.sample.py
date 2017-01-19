# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
BUGZILLA_DATABASE_URI = 'mysql+oursql://bugzilla:bugzilla@localhost/bugzilla'
SETTINGS_DATABASE_URI = 'mysql+oursql://bugzilla:bugzilla@localhost/bugzilla-dashboard'

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"