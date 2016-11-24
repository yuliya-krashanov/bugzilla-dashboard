import datetime
import os
from functools import wraps

from flask import Flask, Response, make_response, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models as m

app = Flask(__name__)

engine = create_engine(DB_URL, pool_recycle=1800)
sm = sessionmaker(bind=engine)

def with_db(f):
    @wraps(f)
    def new_f(*args, **kwargs):
        db = sm()
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    return new_f

@app.route("/")
@with_db
@requires_auth
def index(db):
    projects = map((lambda p: {'id': p.id, 'name': p.name}),
                   db.query(m.Product).filter(m.Product.isactive == 1).all())
    return render_template("index.html", projects=projects)


if __name__ == "__main__":
    app.run(debug=True)