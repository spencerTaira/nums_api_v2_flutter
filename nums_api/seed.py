from nums_api import app
from nums_api.database import db
from nums_api.trivia.models import Trivia
from nums_api.maths.models import Math
from nums_api.dates.models import Date
from nums_api.years.models import Year

# import all models - necessary for create_all()

db.drop_all()
db.create_all()
