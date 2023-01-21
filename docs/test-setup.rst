Running and Organizing Tests
============================

Route and Model tests will live in separate files within a test directory
in each app ::

  dates/tests/test_routes.py
  dates/tests/test_models.py

Use the -v flag for verbose test output

Run all tests files ::

  python -m unittest discover
  python -m unittest discover -v

Run tests within a test directory ::

  python -m unittest
  python -m unittest -v

Run a single test file within a test directory ::

  python -m unittest TEST_FILE_NAME.py
  python -m unittest -v TEST_FILE_NAME.py
