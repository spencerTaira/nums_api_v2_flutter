from flask import Flask, request
from flask_cors import CORS

from nums_api.config import DATABASE_URL
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root
from nums_api.limiter import limiter

# create app and add configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# register blueprints
app.register_blueprint(trivia, url_prefix="/api/trivia")
app.register_blueprint(math, url_prefix="/api/math")
app.register_blueprint(dates, url_prefix="/api/dates")
app.register_blueprint(years, url_prefix="/api/years")
app.register_blueprint(root, url_prefix="/")

limiter.init_app(app)


def is_testing_env():
    """ Return bool of whether config['TESTING'] is true """
    return app.config["TESTING"]


@app.before_request
def set_API_rate_limit():
    """ Setting API rate limit for each route
        Per endpoint, limit is 200 per day.
        When in a testing environment, per endpoint, limit is 5 per minute
    """
    if not is_testing_env():
        if request.path != '/':
            limiter.limit("200 per day")(lambda: None)()
    else:
        if request.path != '/':
            limiter.limit("5 per minute")(lambda: None)()


# allow CORS and connect app to database
CORS(app)
connect_db(app)
