from datetime import datetime
from nums_api.database import db


class Math(db.Model):
    """Math facts about numbers."""

    __tablename__ = "math"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    number = db.Column(
        db.Numeric,
        nullable=False,
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False,
        unique=True,
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
        nullable=False,
        unique=True,
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


class MathLikeCounter(db.Model):
    """Keeps track of amount of likes per fact"""

    __tablename__ = "math_like_counters"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    math_id = db.Column(
        db.Integer,
        db.ForeignKey("math.id"),
        unique=True,
        nullable=False
    )

    num_likes = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    math = db.relationship(
        "Math", 
        backref=db.backref("like_counter", uselist=False)
    )

    def increment_likes(self):
        self.num_likes += 1
