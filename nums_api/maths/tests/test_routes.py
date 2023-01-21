from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math,MathLikeCounter
from nums_api.__init__ import limiter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class MathBaseRouteTestCase(TestCase):
    """
        Houses setup functionality for math route tests.
        Should be subclassed for any math route classes utilized.
    """

    def setUp(self):
        """Set up test data here"""
        
        MathLikeCounter.query.delete()
        Math.query.delete()

        self.m1 = Math(
            number=1,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1 is the number for this m1 test fact statement.",
            was_submitted=False,
        )

        self.m2 = Math(
            number=2.22,
            fact_fragment="the number for this m2 test fact fragment",
            fact_statement="2.22 is the number for this m2 test fact statement.",
            was_submitted=False,
        )

        db.session.add_all([self.m1, self.m2])
        db.session.commit()

        self.client = app.test_client()

        # disable API rate limits for tests
        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


class MathRouteTestCase(MathBaseRouteTestCase):

    def test_setup(self):
        """Test to make sure tests are set up correctly"""

        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_math_fact_for_int(self):
        with self.client as c:

            resp = c.get("/api/math/1")
            expected_resp = {
                "fact": {
                    "fragment": "the number for this m1 test fact fragment",
                    "statement": "1 is the number for this m1 test fact statement.",
                    "number": 1,
                    "type": "math"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_get_math_fact_for_float(self):
        with self.client as c:

            resp = c.get("/api/math/2.22")
            expected_resp = {
                "fact": {
                    "fragment": "the number for this m2 test fact fragment",
                    "statement": "2.22 is the number for this m2 test fact statement.",
                    "number": 2.22,
                    "type": "math"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_get_math_fact_not_found(self):
        with self.client as c:

            resp = c.get("/api/math/-1")
            expected_resp = {
                "error": {
                    "message": "A math fact for -1 not found",
                    "status": 404
                }
            }

            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, expected_resp)

    def test_get_math_fact_invalid_number(self):
        with self.client as c:

            resp = c.get("/api/math/one")

            self.assertEqual(resp.status_code, 400)

    def test_get_math_fact_random(self):
        with self.client as c:

            resp = c.get("/api/math/random")

            possible_resp_1 = {
                "fact": {
                    "fragment": "the number for this m1 test fact fragment",
                    "statement": "1 is the number for this m1 test fact statement.",
                    "number": 1,
                    "type": "math"
                }
            }

            possible_resp_2 = {
                "fact": {
                    "fragment": "the number for this m2 test fact fragment",
                    "statement": "2.22 is the number for this m2 test fact statement.",
                    "number": 2.22,
                    "type": "math"
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertIn(resp.json, [possible_resp_1, possible_resp_2])

    def test_add_math_like(self):
        """Test the like route."""
        with self.client as c:

            resp = c.post(f"api/math/like/{self.m1.id}")
            self.assertEqual(resp.status_code, 200)

            ml1 = MathLikeCounter.query.filter_by(math_id=self.m1.id).one()
            self.assertEqual(ml1.num_likes, 1)

            resp = c.post(f"api/math/like/{self.m1.id}")
            self.assertEqual(resp.status_code, 200)

            ml1 = MathLikeCounter.query.filter_by(math_id=self.m1.id).one()
            self.assertEqual(ml1.num_likes, 2)

    def test_add_math_like_fail(self):
        """Test like route failure."""
        with self.client as c:

            resp = c.post(f"api/math/like/{-1}")
            self.assertEqual(resp.status_code, 404)
