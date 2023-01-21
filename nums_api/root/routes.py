from flask import Blueprint, render_template
from markdown import markdown
from pathlib import Path

# get the absolute path to the nums_api package directory
# it's two levels up from the location of this module
nums_api_path = Path(__file__).parent.parent.absolute()

root = Blueprint("root", __name__)

@root.get("/")
def root_route():
    """Render html with API docs from markdown file."""

    with open(f"{nums_api_path}/static/docs/api-documentation.md", "r") as f:
        text = f.read()
        api_docs = markdown(text)

    return render_template("index.html", api_docs=api_docs)
