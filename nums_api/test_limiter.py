from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year
from nums_api.trivia.models import Trivia
from nums_api.dates.models import Date
from nums_api.maths.models import Math
from nums_api.__init__ import limiter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class LimiterBaseTestCase(TestCase):
    """
        Houses setup functionality.
    """

    def setUp(self):
        """Set up test data here"""
        Year.query.delete()
        Trivia.query.delete()
        Date.query.delete()
        Math.query.delete()

        self.y1 = Year(
            year=2019,
            fact_fragment="is the year COVID was detected",
            fact_statement="2019 is the year COVID was first detected.",
            was_submitted=False
        )

        self.t1 = Trivia(
            number=1,
            fact_fragment="the number for this t1 test fact fragment",
            fact_statement="1 is the number for this t1 test fact statement.",
            was_submitted=False
        )

        self.m1 = Math(
            number=1.5,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1.5 is the number for m1 this test fact statement.",
            was_submitted=False
        )

        self.d1 = Date(
            day_of_year=2,
            year=2000,
            fact_fragment="the number for this d1 test fact fragment",
            fact_statement="2 is the number for this d1 test fact statement",
            was_submitted=False
        )

        db.session.add_all([self.y1, self.t1, self.m1, self.d1])
        db.session.commit()

        self.client = app.test_client()

        limiter.enabled = True

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


class LimiterTestCase(LimiterBaseTestCase):

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        db.session.commit()
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_root_excluded_from_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit 
            # (rate limit applies to diff. routes)
            for i in range(5):
                resp = c.get("/")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

    def test_trivia_num_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/trivia/1")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/trivia/1")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/trivia/3")
            self.assertEqual(resp.status_code, 429)

    def test_trivia_random_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/trivia/random")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/trivia/random")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/trivia/random")
            self.assertEqual(resp.status_code, 429)

    def test_year_num_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/years/2019")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/years/2019")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/years/2019")
            self.assertEqual(resp.status_code, 429)

    def test_year_random_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/years/random")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/years/random")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/years/random")
            self.assertEqual(resp.status_code, 429)

    def test_dates_num_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/dates/1/2")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/dates/1/2")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/dates/1/2")
            self.assertEqual(resp.status_code, 429)

    def test_dates_random_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/dates/random")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/dates/random")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/dates/random")
            self.assertEqual(resp.status_code, 429)

    def test_maths_num_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/math/1.5")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/math/1.5")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/math/1.5")
            self.assertEqual(resp.status_code, 429)

    def test_maths_random_rate_limit(self):
        with self.client as c:
            # Send a number of requests within the rate limit
            for i in range(5):
                resp = c.get("/api/math/random")
                self.assertEqual(resp.status_code, 200)

            # Send a request that exceeds the rate limit
            resp = c.get("/api/math/random")
            self.assertEqual(resp.status_code, 429)

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

            # Send a req that exceeds the rate limit after different route req
            resp = c.get("/api/math/random")
            self.assertEqual(resp.status_code, 429)
