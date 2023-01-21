from unittest import TestCase
from nums_api import app
from nums_api.database import db, connect_db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date, DateLikeCounter

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

db.drop_all()
db.create_all()


class DateModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        DateLikeCounter.query.delete()
        Date.query.delete()

        self.d1 = Date(
            day_of_year=60,
            year=2000,
            fact_fragment="the number for this d1 test fact fragment",
            fact_statement="60 is the number for this d1 test fact statement",
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
        """Test to make sure record is inserted into the database correctly"""
        self.assertIsInstance(self.d1, Date)
        self.assertEqual(Date.query.count(), 0)

        db.session.add(self.d1)
        db.session.commit()

        self.assertEqual(Date.query.count(), 1)
        self.assertEqual(
            Date
            .query
            .filter_by(day_of_year=60)
            .one()
            .day_of_year, 60
        )

    def test_date_to_day_of_year(self):
        """ Test to check correct day of year is given from class method
            date_from_day_of_year
        """

        day_of_year = Date.date_to_day_of_year(1, 1)
        self.assertEqual(day_of_year, 1)

        day_of_year = Date.date_to_day_of_year(2, 28)
        self.assertEqual(day_of_year, 59)

        day_of_year = Date.date_to_day_of_year(2, 29)
        self.assertEqual(day_of_year, 60)

        day_of_year = Date.date_to_day_of_year(3, 1)
        self.assertEqual(day_of_year, 61)

        day_of_year = Date.date_to_day_of_year(12, 31)
        self.assertEqual(day_of_year, 366)

    def test_invalid_type_date_to_day_of_year(self):
        """ Test to check correct error response is given when invalid data type
            is used as input
        """

        with self.assertRaises(TypeError) as cm:
            Date.date_to_day_of_year(1.1, 1)

        self.assertTrue(isinstance(cm.exception, TypeError))
        self.assertEqual("Invalid data types", str(cm.exception))

        with self.assertRaises(TypeError) as cm:
            Date.date_to_day_of_year(1, 'a')

        self.assertTrue(isinstance(cm.exception, TypeError))
        self.assertEqual("Invalid data types", str(cm.exception))

    def test_out_of_range_input_date_to_day_of_year(self):
        """ Test to check correct error response is given when out of range data
            is used as input
        """
        with self.assertRaises(ValueError) as cm:
            Date.date_to_day_of_year(13, 1)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("13 is an invalid month", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            Date.date_to_day_of_year(-1, 1)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("-1 is an invalid month", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            Date.date_to_day_of_year(1, 0)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("0 is an invalid day", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            Date.date_to_day_of_year(1, 40)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("40 is an invalid day", str(cm.exception))

    def test_get_date_from_day_of_year(self):
        """ Test to check correct month and day is given from class method
            date_from_day_of_year
        """
        (month, day) = Date.date_from_day_of_year(10)
        self.assertEqual(month, 1)
        self.assertEqual(day, 10)

        (month, day) = Date.date_from_day_of_year(4)
        self.assertEqual(month, 1)
        self.assertEqual(day, 4)

        (month, day) = Date.date_from_day_of_year(61)
        self.assertEqual(month, 3)
        self.assertEqual(day, 1)

        (month, day) = Date.date_from_day_of_year(366)
        self.assertEqual(month, 12)
        self.assertEqual(day, 31)

        (month, day) = Date.date_from_day_of_year(60)
        self.assertEqual(month, 2)
        self.assertEqual(day, 29)

    def test_invalid_type_date_from_day_of_year(self):
        """ Test to check correct error response is given when invalid data type
            is used as input
        """

        with self.assertRaises(TypeError) as cm:
            Date.date_from_day_of_year('a')

        self.assertTrue(isinstance(cm.exception, TypeError))
        self.assertEqual("Invalid data type", str(cm.exception))

        with self.assertRaises(TypeError) as cm:
            Date.date_from_day_of_year(123123.2353)

        self.assertTrue(isinstance(cm.exception, TypeError))
        self.assertEqual("Invalid data type", str(cm.exception))

    def test_out_of_range_data_date_from_day_of_year(self):
        """ Test to check correct error response is given when out of range data
            is used as input
        """

        with self.assertRaises(ValueError) as cm:
            Date.date_from_day_of_year(0)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("""0 is out of range, does not exists
                in current calendar""", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            Date.date_from_day_of_year(367)

        self.assertTrue(isinstance(cm.exception, ValueError))
        self.assertEqual("""367 is out of range, does not exists
                in current calendar""", str(cm.exception))

    def test_add_likes(self):
        """Makes sure the like feature works"""

        db.session.add(self.d1)
        db.session.commit()

        l1 = DateLikeCounter(date_id=self.d1.id)

        db.session.add(l1)

        db.session.commit()

        num_likes = self.d1.like_counter.num_likes
        self.assertEqual(num_likes, 0)

        self.d1.like_counter.increment_likes()
        db.session.commit()

        num_likes = self.d1.like_counter.num_likes
        self.assertEqual(num_likes, 1)

        self.d1.like_counter.increment_likes()
        db.session.commit()

        num_likes = self.d1.like_counter.num_likes
        self.assertEqual(num_likes, 2)
