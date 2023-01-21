from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.trivia.models import Trivia, TriviaLikeCounter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

db.drop_all()
db.create_all()


class TriviaModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        TriviaLikeCounter.query.delete()
        Trivia.query.delete()

        self.t1 = Trivia(
            number=1,
            fact_fragment="the number for this t1 test fact fragment",
            fact_statement="1 is the number for this t1 test fact statement.",
            was_submitted=False,
        )

        self.t2 = Trivia(
            number=2,
            fact_fragment="the magic number for this t2 test fact fragment",
            fact_statement="2 is the magic number for this t2 test fact statement.",
            was_submitted=False,
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model(self):
        self.assertIsInstance(self.t1, Trivia)
        self.assertEqual(Trivia.query.count(), 0)

        db.session.add(self.t1)
        db.session.commit()

        self.assertEqual(Trivia.query.count(), 1)
        self.assertEqual(Trivia.query.filter_by(number=1).one().number, 1)

    def test_add_likes(self):
        """Makes sure the like feature works"""

        db.session.add(self.t1)
        db.session.add(self.t2)
        db.session.commit()

        l1 = TriviaLikeCounter(trivia_id=self.t1.id)
        l2 = TriviaLikeCounter(trivia_id=self.t2.id)

        db.session.add(l1)
        db.session.add(l2)
        db.session.commit()

        num_likes = self.t2.like_counter.num_likes
        self.assertEqual(num_likes, 0)

        self.t2.like_counter.increment_likes()
        db.session.commit()

        num_likes = self.t2.like_counter.num_likes
        self.assertEqual(num_likes, 1)

        num_likes = self.t1.like_counter.num_likes
        self.assertEqual(num_likes, 0)


