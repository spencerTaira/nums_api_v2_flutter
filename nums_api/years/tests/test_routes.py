from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year, YearLikeCounter
from nums_api.__init__ import limiter


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class YearBaseRouteTestCase(TestCase):
    """
        Houses setup functionality.
        Should be subclassed for any year route classes utilized
    """

    def setUp(self):
        """Set up test data here"""

        YearLikeCounter.query.delete()
        Year.query.delete()

        self.y1 = Year(
            year=2019,
            fact_fragment="is the year COVID was detected",
            fact_statement="2019 is the year COVID was first detected.",
            was_submitted=False
        )

        db.session.add(self.y1)
        db.session.commit()

        self.client = app.test_client()

        # disable API rate limits for tests
        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


class YearRouteTestCase(YearBaseRouteTestCase):

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_year_fact(self):
        with self.client as c:
            resp = c.get("/api/years/2019")
            expected_resp = {
                "fact": {
                    "fragment": "is the year COVID was detected",
                    "statement": "2019 is the year COVID was first detected.",
                    "year": 2019,
                    "type": "year"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_get_year_fact_not_found(self):
        with self.client as c:

            resp = c.get("/api/years/2200")
            expected_resp = {
                "error": {
                    "message": "A fact for 2200 not found",
                    "status": 404
                }
            }

            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, expected_resp)

    def test_get_year_fact_not_valid_number(self):
        with self.client as c:

            resp = c.get("/api/years/asdf")

            self.assertEqual(resp.status_code, 404)

    def test_get_random_year_fact(self):
        with self.client as c:

            resp = c.get("/api/years/random")
            expected_resp = {
                "fact": {
                    "fragment": "is the year COVID was detected",
                    "statement": "2019 is the year COVID was first detected.",
                    "year": 2019,
                    "type": "year"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_add_year_like(self):
        """Test the like route."""
        with self.client as c:

            resp = c.post(f"api/years/like/{self.y1.id}")
            self.assertEqual(resp.status_code, 200)

            yl1 = YearLikeCounter.query.filter_by(year_id=self.y1.id).one()
            self.assertEqual(yl1.num_likes, 1)

            resp = c.post(f"api/years/like/{self.y1.id}")
            self.assertEqual(resp.status_code, 200)

            yl1 = YearLikeCounter.query.filter_by(year_id=self.y1.id).one()
            self.assertEqual(yl1.num_likes, 2)

    def test_add_year_like_fail(self):
        """Test like route failure."""
        with self.client as c:

            resp = c.post(f"api/years/like/{-1}")
            self.assertEqual(resp.status_code, 404)
