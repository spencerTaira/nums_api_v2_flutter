from datetime import datetime
from nums_api.database import db


class Date (db.Model):
    """Date facts."""

    __tablename__ = "dates"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    # store date as integer that represents the 1-indexed day of a leap year
    # 1 - 366: February 28th is always 59 & March 1st is always 61
    # can't use date field, we're dealing with some historical dates- think about
    # the calendar changes across history (Postgres  follows the Gregorian
    # calendar rules for all dates,)
    day_of_year = db.Column(
        db.Integer,
        nullable=False,
    )

    year = db.Column(
        db.Integer,
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
        nullable=False,
    )

    added_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    was_submitted = db.Column(
        db.Boolean,
        nullable=False,
    )

    @classmethod
    def date_to_day_of_year(cls, month, day):
        """
        Converts month (int) and day (int) to day of the year (1-366) (int)

        Returns day of the year.
        """
        # This maps valid days for each month
        valid_days_for_months = {
            1: 31,
            2: 29,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        # This maps the months to their respective first day of the year
        month_to_first_day_of_year = {
            1: 1,
            2: 32,
            3: 61,
            4: 92,
            5: 122,
            6: 153,
            7: 183,
            8: 214,
            9: 245,
            10: 275,
            11: 306,
            12: 336,
        }

        if not(isinstance(month, int) and isinstance(day, int)):
            raise TypeError("Invalid data types")

        if not valid_days_for_months.get(month, None):
            raise ValueError(f"{month} is an invalid month")

        if day > valid_days_for_months[month] or day < 1:
            raise ValueError(f"{day} is an invalid day")

        # Subtract 1 since days are 1-indexed
        day_of_year = month_to_first_day_of_year[month] + day - 1

        return day_of_year

    @classmethod
    def date_from_day_of_year(cls, day_of_year):
        """
            Converts day_of_year (int) to (month:int, day:int).

            Returns (month:int, day:int)
        """

        day_of_year_to_month = {
            1: 1,
            32: 2,
            61: 3,
            92: 4,
            122: 5,
            153: 6,
            183: 7,
            214: 8,
            245: 9,
            275: 10,
            306: 11,
            336: 12,
        }

        if not isinstance(day_of_year, int):
            raise TypeError("Invalid data type")

        if day_of_year < 1 or day_of_year > 366:
            raise ValueError(
                f"""{day_of_year} is out of range, does not exists
                in current calendar""")

        first_of_each_month = list(day_of_year_to_month.keys())

        for index, first in enumerate(first_of_each_month):
            month = day_of_year_to_month[first]
            day = day_of_year + 1 - first_of_each_month[index]

            if day_of_year is first:
                return (month, 1)
            if index is len(day_of_year_to_month) - 1:
                return (month, day)
            if day_of_year > first and day_of_year < first_of_each_month[index+1]:
                return (month, day)

        raise Exception("Should not get here - encountered unexpected error.")


class DateLikeCounter(db.Model):
    """Keeps track of amount of likes per fact"""

    __tablename__ = "date_like_counters"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    date_id = db.Column(
        db.Integer,
        db.ForeignKey("dates.id"),
        unique=True,
        nullable=False
    )

    num_likes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    date = db.relationship(
        "Date",
        backref=db.backref("like_counter", uselist=False)
    )

    def increment_likes(self):
        self.num_likes += 1
