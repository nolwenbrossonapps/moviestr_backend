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

- POST signup: If ok, add tokens to cookies
- POST login: If ok, add tokens to cookies
- POST logout: Delete tokens 