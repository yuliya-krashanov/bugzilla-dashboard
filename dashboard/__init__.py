from flask import Flask


app = Flask(__name__)
app.config.from_object('config')
app.url_map.strict_slashes = False


from dashboard.database import *
from dashboard.admin import *
from dashboard.views import *

init_admin_login()


@app.teardown_appcontext
def shutdown_session(exception=None):
    bugzilla_db.remove()
    settings_db.remove()
