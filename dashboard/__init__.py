from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('sheduler_settings')
app.url_map.strict_slashes = False

# Sheduler jobs run
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


from dashboard.database import *
from dashboard.admin import *
from dashboard.views import *

init_admin_login()


@app.teardown_appcontext
def shutdown_session(exception=None):
    bugzilla_db.remove()
    settings_db.remove()
