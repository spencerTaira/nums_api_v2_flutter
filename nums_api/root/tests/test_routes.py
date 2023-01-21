from unittest import TestCase
from nums_api import app

# Make Flask errors be real errors, not HTML pages with error info
app.config["TESTING"] = True


class RootRouteTestCase(TestCase):
    """Test root route."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()

    def test_root_route_favicon(self):
        """Makes sure that the favicon is present"""

        with self.client as client:
            response = client.get("/")
            html = response.get_data(as_text=True)
            self.assertIn("favicon.png", html)

    def test_root_route_markdown(self):
        """Makes sure that markdown file content is present"""

        with self.client as client:
            response = client.get("/")
            html = response.get_data(as_text=True)
            self.assertIn(
                "<!-- API Documentation - Comment for testing purposes -->", html
            )
