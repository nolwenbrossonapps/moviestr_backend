# Basic configurations

New venv:
- python -m venv .venv
- source .venv/bin/activate


To run the app:
- export FLASK_APP=app.py
- export FLASK_DEBUG=1
- flask run

Docs:
- https://docs.mongoengine.org/guide/defining-documents.html

Local container to avoid installing mongodb:
- docker run -p 27017:27017 -v moviestr_authent:/data/db mongo


# Next steps:

- Both stateless and stateful requests are now working with Token check.
- To test: In postman, make a POST token, keep the csrf token in header, and make a POST token/access
- Next steps: Improve the logic of signup, login, logout + Drop the token examples that should be in the Doc.