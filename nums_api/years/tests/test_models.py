from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year, YearLikeCounter
from sqlalchemy.exc import DataError

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

db.drop_all()
db.create_all()


class YearModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        YearLikeCounter.query.delete()
        Year.query.delete()

        self.y1 = Year(
            year=2023,
            fact_fragment="the year for this y1 test fact_fragment",
            fact_statement="2023 is the year for this y1 test fact statement.",
            was_submitted=False
        )

        self.y2 = Year(
            year="abcd",
            fact_fragment="",
            fact_statement="",
            was_submitted=False
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model_valid_data(self):
        """Test valid data """
        self.assertIsInstance(self.y1, Year)
        self.assertEqual(Year.query.count(), 0)

        db.session.add(self.y1)
        db.session.commit()

        self.assertEqual(Year.query.count(), 1)

        year_obj = Year.query.filter_by(year=2023).one()

        self.assertEqual(year_obj.year, 2023)
        self.assertEqual(year_obj.fact_fragment,
                         "the year for this y1 test fact_fragment")
        self.assertEqual(year_obj.fact_statement,
                         "2023 is the year for this y1 test fact statement.")
        self.assertEqual(year_obj.was_submitted, False)

    def test_model_invalid_data(self):
        """Test invalid data"""
        self.assertEqual(Year.query.count(), 0)

        with self.assertRaises(DataError):
            db.session.add(self.y2)
            db.session.commit()

            db.session.rollback()

            year_obj = Year.query.all()
            self.assertEqual(len(year_obj), 0)

    def test_add_likes(self):
        """Makes sure the like feature works"""

        db.session.add(self.y1)
        db.session.commit()

        l1 = YearLikeCounter(year_id=self.y1.id)

        db.session.add(l1)
        db.session.commit()

        num_likes = self.y1.like_counter.num_likes
        self.assertEqual(num_likes, 0)

        self.y1.like_counter.increment_likes()
        db.session.commit()

        num_likes = self.y1.like_counter.num_likes
        self.assertEqual(num_likes, 1)
