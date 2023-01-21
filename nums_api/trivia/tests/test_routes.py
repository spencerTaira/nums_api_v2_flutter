from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.trivia.models import Trivia, TriviaLikeCounter
from nums_api.config import DATABASE_URL_TEST
from nums_api.__init__ import limiter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class TriviaBaseRouteTestCase(TestCase):
    """
    Houses setup functionality.
    Should be subclassed for any trivia route classes utilized
    """

    def setUp(self):
        """Set up test data here"""

        TriviaLikeCounter.query.delete()
        Trivia.query.delete()

        self.t1 = Trivia(
            number=1,
            fact_fragment="the loneliest number",
            fact_statement="1 is the loneliest number.",
            was_submitted=True,
        )

        db.session.add(self.t1)
        db.session.commit()

        self.client = app.test_client()

        # disable API rate limits for tests
        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


class TriviaRouteTestCase(TriviaBaseRouteTestCase):
    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_trivia_fact(self):
        with self.client as c:

            resp = c.get("/api/trivia/1")
            expected_resp = {
                "fact": {
                    "fragment": "the loneliest number",
                    "statement": "1 is the loneliest number.",
                    "number": 1,
                    "type": "trivia",
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_get_trivia_fact_not_found(self):
        with self.client as c:

            resp = c.get("/api/trivia/10")
            expected_resp = {
                "error": {
                    "message": "A trivia fact for 10 not found",
                    "status": 404
                }
            }

            self.assertEqual(resp.status_code, 404)
            self.assertEqual(resp.json, expected_resp)

    def test_get_trivia_fact_not_valid_number(self):
        with self.client as c:

            resp = c.get("/api/trivia/a")

            self.assertEqual(resp.status_code, 404)

    def test_get_random_trivia_fact(self):
        with self.client as c:

            resp = c.get("/api/trivia/random")
            expected_resp = {
                "fact": {
                    "fragment": "the loneliest number",
                    "statement": "1 is the loneliest number.",
                    "number": 1,
                    "type": "trivia",
                }
            }

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, expected_resp)

    def test_add_trivia_like(self):
        """Test the like route."""
        with self.client as c:

            resp = c.post(f"api/trivia/like/{self.t1.id}")
            self.assertEqual(resp.status_code, 200)

            tl1 = TriviaLikeCounter.query.filter_by(trivia_id=self.t1.id).one()
            self.assertEqual(tl1.num_likes, 1)

            resp = c.post(f"api/trivia/like/{self.t1.id}")
            self.assertEqual(resp.status_code, 200)

            tl1 = TriviaLikeCounter.query.filter_by(trivia_id=self.t1.id).one()
            self.assertEqual(tl1.num_likes, 2)

    def test_add_trivia_like_fail(self):
        """Test like route failure."""
        with self.client as c:

            resp = c.post(f"api/trivia/like/{-1}")
            self.assertEqual(resp.status_code, 404)
