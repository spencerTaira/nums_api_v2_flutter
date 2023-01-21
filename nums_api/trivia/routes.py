from flask import Blueprint, jsonify
from nums_api.trivia.models import Trivia, TriviaLikeCounter
import random
from nums_api.database import db

trivia = Blueprint("trivia", __name__)


@trivia.get("/<int:number>")
def get_trivia_fact(number):
    """
    Get trivia fact about specific number
        Input: number (int)
        Output: JSON like
        {
            "fact": {
                "fragment": "the atomic number of Unquadpentium",
                "statement": "145 is the atomic number of Unquadpentium.",
                "number": 145,
                "type": "trivia"
            }
        }

        OR If number is not found...
        Output: JSON like
        {
            error: {
                    "message": f"A trivia fact for { number } not found",
                    "status": 404
                    }
        }
    """
    trivia_facts = Trivia.query.filter(Trivia.number == number).all()

    if not trivia_facts:
        error = {
            "message": f"A trivia fact for { number } not found",
            "status": 404
        }

        return (jsonify(error=error), 404)

    fact = random.choice(trivia_facts)

    fact_data = {
        "fragment": fact.fact_fragment,
        "statement": fact.fact_statement,
        "number": fact.number,
        "type": "trivia"
    }

    return jsonify(fact=fact_data)


@trivia.get("/random")
def get_trivia_fact_random():
    """
    Get trivia fact about random number
       Output: JSON like
       {
           "fact": {
               "fragment": "the atomic number of Unquadpentium",
               "statement": "145 is the atomic number of Unquadpentium.",
               "number": 145,
               "type": "trivia"
           }
       }
    """

    trivia_facts = Trivia.query.all()
    fact = random.choice(trivia_facts)

    fact_data = {
        "fragment": fact.fact_fragment,
        "statement": fact.fact_statement,
        "number": fact.number,
        "type": "trivia",
    }

    return jsonify(fact=fact_data)


@trivia.post("/like/<int:id>")
def add_trivia_like(id):
    """
    Post like a trivia fact
        Input: id (int)
        Output: "You have liked this fact."

        OR If number with id is not found...
        Output: JSON like
        {
        error: {
            "message": f"A trivia fact for id { id } not found",
            "status": 404
            }
        }
    """

    fact = Trivia.query.get(id)

    if not fact:
        error = {
            "message": f"A trivia fact for id { id } not found",
            "status": 404
        }
        return (jsonify(error), 404)

    like_counter = TriviaLikeCounter.query.filter_by(trivia_id=fact.id).first()

    if not like_counter:
        like_counter = TriviaLikeCounter(trivia_id=id)
        db.session.add(like_counter)
        db.session.commit()

    like_counter.increment_likes()
    db.session.commit()

    return ("You have liked this fact.", 200)
