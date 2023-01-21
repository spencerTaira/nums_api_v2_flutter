from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math, MathLikeCounter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class MathModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        MathLikeCounter.query.delete()
        Math.query.delete()

        self.m1 = Math(
            number=1.5,
            fact_fragment="the number for this m1 test fact fragment",
            fact_statement="1.5 is the number for m1 this test fact statement.",
            was_submitted=False
        )

        self.m2 = Math(
            number=3,
            fact_fragment="the number for this m2 test fact fragment",
            fact_statement="3 is the number for m2 this test fact statement.",
            was_submitted=False
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model(self):
        self.assertIsInstance(self.m1, Math)
        self.assertEqual(Math.query.count(), 0)

        db.session.add(self.m1)
        db.session.commit()

        self.assertEqual(Math.query.count(), 1)
        self.assertEqual(Math.query.filter_by(number=1.5).one().number, 1.5)

    def test_add_likes(self):
        """Makes sure the like feature works"""

        db.session.add(self.m1)
        db.session.add(self.m2)
        db.session.commit()

        l1 = MathLikeCounter(math_id=self.m1.id)
        l2 = MathLikeCounter(math_id=self.m2.id)

        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        num_likes = self.m2.like_counter.num_likes
        self.assertEqual(num_likes, 0)

        self.m2.like_counter.increment_likes()
        db.session.commit()

        num_likes = self.m2.like_counter.num_likes
        self.assertEqual(num_likes, 1)

        num_likes = self.m1.like_counter.num_likes
        self.assertEqual(num_likes, 0)
