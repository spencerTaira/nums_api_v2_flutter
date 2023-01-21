import os
import json
from nums_api.dates.models import Date
from nums_api.years.models import Year
from nums_api.maths.models import Math
from nums_api.trivia.models import Trivia
from nums_api.database import db
import datetime

def format_text_to_csv(directory):
    """
    Creates/Edits readable CSV files from text files

    Separates values by "*"

    Input:
        - directory (string)
    """

    files = os.listdir(f"./{directory}")

    for file in files:
        (filename, extension) = os.path.splitext(file)

        result = None

        if extension == ".txt":
            with open(f"./{directory}/{file}") as f:
                text = f.read()
                result = json.loads(text)

            with open(f"./{directory}/{filename}.csv", "w") as f:
                for key in result.keys():
                    for fact in result[key]:
                        f.write("%s*%s\n"%(key, fact))


def normalize_data(data):
    """
    Converts lists of facts into the right format to insert into our database

    Input:
        - data like:
            {
                "24": [{
                        "text": "Text.",
                        "self": false,
                        "pos": "N",
                    }, ...], ...
            }

    Output:
        normalized data like:
            {
                "24": [{
                        "number": 24,
                        "fact_fragment": "text",
                        "fact_statement": "text.",
                        "was_submitted": False,
                    }, ...], ...
            }

    """

    clean_data = filter_data(data)

    for key in clean_data:
        normalized_facts = []

        for fact in clean_data[key]:
            result = normalize_fact(key, fact)

            if result:
                normalized_facts.append(result)

        clean_data[key] = normalized_facts

    return clean_data


def filter_data(data):
    """
    Cleans data of unwanted facts and empty lists

    Input:
        - data like:
            {
                "24": [{
                        "text": "Text.",
                        "self": false,
                        "pos": "N",
                    }, ...], ...
            }

    Output:
        same data without elements with "self": true and without empty lists
    """

    # Filtering out dicts with "self": true
    for key in data:
        filtered_facts = [fact for fact in data[key] if fact["self"] == False]
        data[key] = filtered_facts

    # Filtering out empty lists
    filtered_data = {key: data[key] for key in data if data[key] != []}

    return filtered_data


def normalize_fact(number, fact):
    """
    Converts original data into a data shape we can input into the database

    Input:
        - number (string)
        - fact like:
            {
                "text": ...,
                "self": False,
                "pos": ("DET", "N", "NP", "ADV", "V"),
                "year" ...,
            }

    Output:
        - Math, Trivia, and Year Model
            {
                "number",
                "fact_fragment",
                "fact_statement",
                "was_submitted",
            }
        - Date Model
            {
                "number",
                "fact_fragment",
                "fact_statement",
                "was_submitted",
                "year",
            }
    """

    normalized_fact = {}

    text = fact["text"]

    if fact.get("pos") != "NP":
        first_char = text[0].lower()
        text = first_char + text[1:]

    last_char = text[-1]
    last_char_code = ord(last_char)

    if last_char == ".":
        text = text[:-1]

    # Filter out results that do not end in ".", ")", or alphanumeric characters
    # as they most likely consist of complex grammar we do not support
    elif (
        (last_char_code < ord("a") or last_char_code > ord("z")) and
        (last_char_code < ord("A") or last_char_code > ord("Z")) and
        (last_char_code < ord("0") or last_char_code > ord("9")) and
        last_char != ")" and
        last_char != '"' and
        last_char != "'"
    ):
        return None

    prefix = get_prefix(number, fact)

    normalized_fact["number"] = int(number)
    normalized_fact["fact_fragment"] = text
    normalized_fact["fact_statement"] = f"{prefix} {text}."
    normalized_fact["was_submitted"] = False

    if direc == "dates":
        normalized_fact["year"] = fact["year"]

    return normalized_fact


def get_prefix(number, fact):
    """
    Concatenates numbers with a prefix that is used for fact_statements

    Input:
        - number (string)
        - fact like:
            {
                "text": ...,
                "self": False,
                "pos": ("DET", "N", "NP", "ADV", "V"),
                "year" ...,
            }

    Output: string
    """

    number = int(number)
    MONTH_NAMES = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    if direc == "math" or direc == "trivia":
        return f"{number} is"
    elif direc == "dates":
        (month_num, day_num) = Date.date_from_day_of_year(number)
        month_name = MONTH_NAMES[month_num - 1]
        num_ordinal_suff = get_ordinal_suffix(day_num)

        if fact["year"] < 0:
            return (
                f"{month_name} {num_ordinal_suff} is the day in {-fact['year']} BC that"
            )
        else:
            return (
                f"{month_name} {num_ordinal_suff} is the day in {fact['year']} that"
            )
    elif direc == "years":
        curr_year = datetime.date.today().year

        if number < 0:
            return f"{-number} BC is the year that"
        elif number > curr_year:
            return f"{number} will be the year that"
        else:
            return f"{number} is the year that"


def get_ordinal_suffix(num):
    """
    Concatenates a number with an ordinal suffix

    Input:
        -number: string

    Output: string

    Examples:
        12 -> 12th
        21 -> 21st
        22 -> 22nd
        23 -> 23rd
        24 -> 24th
    """

    number = int(num)

    if number == 11 or number == 12 or number == 13:
        return f"{number}th"
    elif number % 10 == 1:
        return f"{number}st"
    elif number % 10 == 2:
        return f"{number}nd"
    elif number % 10 == 3:
        return f"{number}rd"
    else:
        return f"{number}th"


def insert_data(facts):
    """
    Inserts number and their corresponding facts into PSQL database

    Input:
        -facts like:
            [{
                "number",
                "fact_fragment",
                "fact_statement",
                "was_submitted",
                "year", (for Date model)
            }, ...]
    """

    for fact in facts:
        if direc == "math":
            data = Math(
                number=fact["number"],
                fact_fragment=fact["fact_fragment"],
                fact_statement=fact["fact_statement"],
                was_submitted=fact["was_submitted"]
            )

        elif direc == "trivia":
            data = Trivia(
                number=fact["number"],
                fact_fragment=fact["fact_fragment"],
                fact_statement=fact["fact_statement"],
                was_submitted=fact["was_submitted"]
            )

        elif direc == "years":
            data = Year(
                year=fact["number"],
                fact_fragment=fact["fact_fragment"],
                fact_statement=fact["fact_statement"],
                was_submitted=fact["was_submitted"]
            )

        elif direc == "dates":
            data = Date(
                day_of_year=fact["number"],
                year=fact["year"],
                fact_fragment=fact["fact_fragment"],
                fact_statement=fact["fact_statement"],
                was_submitted=fact["was_submitted"]
            )
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()


def dump_data(directory):
    """
    Controller function that normalizes and inserts data into PSQL database.

    Input:
        -directory (string)
    """

    global direc
    direc = directory

    files = os.listdir(f"./{directory}")

    for file in files:
        (filename, extension) = os.path.splitext(file)

        result = None

        if extension == ".txt":
            with open(f"./{directory}/{file}") as f:
                text = f.read()
                result = json.loads(text)

            normalized_data = normalize_data(result)

            for key in normalized_data:
                insert_data(normalized_data[key])


def format_all_text_to_csv():
    """Formats dates, math, trivia, and years txt files into csv files"""
    format_text_to_csv("dates")
    format_text_to_csv("math")
    format_text_to_csv("trivia")
    format_text_to_csv("years")


def dump_all_data():
    """Dumps dates, math, trivia, and years data into PSQL database"""
    dump_data("math")
    dump_data("trivia")
    dump_data("years")
    dump_data("dates")


# format_all_text_to_csv()
dump_all_data()
