from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date, DateLikeCounter
from nums_api.__init__ import limiter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

db.drop_all()
db.create_all()


class DateBaseRouteTestCase(TestCase):
    """
        Houses setup functionality for Date tests.
        Should be subclassed for any trivia route classes utilized
    """

    def setUp(self):
        """Set up test data here"""

        DateLikeCounter.query.delete()
        Date.query.delete()

        self.d1 = Date(
            day_of_year=1,
            year=2023,
            fact_fragment="the test case",
            fact_statement="January 1st is the test case.",
            was_submitted=True,
        )

        db.session.add(self.d1)
        db.session.commit()

        self.client = app.test_client()

        # disable API rate limits for tests
        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


class DateRouteTestCase(DateBaseRouteTestCase):

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_date_fact(self):
        with self.client as c:

            resp = c.get("/api/dates/1/1")
            expected_resp = {
                "fact": {
                    "fragment": "the test case",
                    "statement": "January 1st is the test case.",
                    "month": 1,
                    "day": 1,
                    "year": 2023,
                    "type": "date"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_get_date_fact_not_found(self):
        with self.client as c:

            resp = c.get("/api/dates/1/2")
            expected_resp = {
                "error": {
                    "message": "A date fact for 1/2 not found",
                    "status": 404
                }
            }

            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, expected_resp)

    def test_get_date_fact_not_valid_number(self):
        with self.client as c:

            resp_month = c.get("/api/dates/a")
            resp_date = c.get("/api/dates/1/t")

            self.assertEqual(resp_month.status_code, 404)
            self.assertEqual(resp_date.status_code, 404)

    def test_get_random_date_fact(self):
        with self.client as c:

            resp = c.get("/api/dates/random")
            expected_resp = {
                "fact": {
                    "fragment": "the test case",
                    "statement": "January 1st is the test case.",
                    "month": 1,
                    "day": 1,
                    "year": 2023,
                    "type": "date"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_out_of_range_date(self):
        with self.client as c:

            resp = c.get("api/dates/13/2")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 400)
            self.assertIn("13 is an invalid month", html)

            resp = c.get("api/dates/1/33")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 400)
            self.assertIn("33 is an invalid day", html)

    def test_add_date_like(self):
        """Test the like route."""
        with self.client as c:

            resp = c.post(f"api/dates/like/{self.d1.id}")
            self.assertEqual(resp.status_code, 200)

            dl1 = DateLikeCounter.query.filter_by(date_id=self.d1.id).one()
            self.assertEqual(dl1.num_likes, 1)

            resp = c.post(f"api/dates/like/{self.d1.id}")
            self.assertEqual(resp.status_code, 200)

            dl1 = DateLikeCounter.query.filter_by(date_id=self.d1.id).one()
            self.assertEqual(dl1.num_likes, 2)

    def test_add_date_like_fail(self):
        """Test like route failure."""
        with self.client as c:

            resp = c.post(f"api/dates/like/{-1}")
            self.assertEqual(resp.status_code, 404)
