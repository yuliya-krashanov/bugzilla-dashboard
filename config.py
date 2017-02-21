import os

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
BUGZILLA_DATABASE_URI = 'mysql+oursql://bugzilla:RyhotfotadHuirf@localhost/bugzilla'
SETTINGS_DATABASE_URI = 'mysql+oursql://sd:Jt71EVDiOG3KUzyg@localhost/stats_dashboard'

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ.get("SD_CSRF_SESSION_KEY", "")

# Secret key for signing cookies
SECRET_KEY = os.environ.get("SD_SECRET_KEY", "")

SERVER_NAME = '127.0.0.1:9006'