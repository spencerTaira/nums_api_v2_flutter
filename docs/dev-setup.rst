Development Environment Setup
=============================

Add a `.env` file in the top level directory and include the following ::

  DATABASE_URL=postgresql:///numbers_api
  DATABASE_URL_TEST=postgresql:///numbers_api_test
  FLASK_APP=nums_api

You'll need Python3 and PostgreSQL ::

  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt

  createdb numbers_api
  createdb numbers_api_test

Install nums_api as a python package in the top level directory ::

  pip install -e .

After installing nums_api delete the nums_api.egg-info/ directory ::

  rm -rf nums_api.egg-info/

When you need to add dependencies to requirements.txt, don't include the
nums_api package as a dependency. To ensure it's not added, update
requirements.txt like this ::

  pip freeze | grep -v github.com > requirements.txt
