from flask import Blueprint, jsonify
from nums_api.maths.models import Math,MathLikeCounter
import random
from werkzeug.exceptions import BadRequest
from nums_api.database import db


math = Blueprint("math", __name__)


@math.get("/<number>")
def get_math_fact(number):
    """
    Get math fact about specific number
        Input: number (int or float)
        Output: JSON like
        {
            "fact": {
                "fragment": "the atomic number of Unquadpentium",
                "statement": "145 is the atomic number of Unquadpentium.",
                "number": 145,
                "type": "math"
            }
        }

        OR If number is not found...
        Output: JSON like
        {
            error: {
                    "message": f"A math fact for { number } not found",
                    "status": 404
                    }
        }
    """

    try:
        num_as_float = float(number)
    except ValueError:
        raise BadRequest("Invalid data: number must be an integer or float")

    math_facts = Math.query.filter(Math.number == num_as_float).all()

    if not math_facts:
        error = {
            "message": f"A math fact for { number } not found",
            "status": 404
        }

        return (jsonify(error=error), 404)

    fact = random.choice(math_facts)

    fact_data = {
        "fragment": fact.fact_fragment,
        "statement": fact.fact_statement,
        "number": float(fact.number),
        "type": "math"
    }

    return jsonify(fact=fact_data)


@math.get("/random")
def get_math_fact_random():
    """
     Get math fact about random number
        Output: JSON like
        {
            "fact": {
                "fragment": "the atomic number of Unquadpentium",
                "statement": "145 is the atomic number of Unquadpentium.",
                "number": 145,
                "type": "math"
            }
        }
    """

    math_facts = Math.query.all()
    fact = random.choice(math_facts)

    fact_data = {
        "fragment": fact.fact_fragment,
        "statement": fact.fact_statement,
        "number": float(fact.number),
        "type": "math"
    }

    return jsonify(fact=fact_data)


@math.post("/like/<int:id>")
def add_math_like(id):
    """
    Post like a math fact
        Input: id (int)
        Output: "You have liked this fact."

        OR If number with id is not found...
        Output: JSON like
        {
            error: {
                    "message": f"A math fact for id { id } not found",
                    "status": 404
                    }
        }
    """

    fact = Math.query.get(id)

    if not fact:
        error = {
            "message": f"A math fact for id { id } not found",
            "status": 404
        }
        return (jsonify(error), 404)

    like_counter = MathLikeCounter.query.filter_by(math_id=fact.id).first()

    if not like_counter:
        like_counter = MathLikeCounter(math_id=id)
        db.session.add(like_counter)
        db.session.commit()

    like_counter.increment_likes()
    db.session.commit()

    return ("You have liked this fact.", 200)
