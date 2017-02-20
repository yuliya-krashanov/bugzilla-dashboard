from flask import Flask

app = Flask(__name__)
app.config.from_object('config.config')
app.url_map.strict_slashes = False

import dashboard.database
import dashboard.views
