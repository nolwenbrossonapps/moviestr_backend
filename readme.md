New venv:
- python -m venv .venv
- source .venv/bin/activate


To run the app:
- export FLASK_APP=src
- export FLASK_DEBUG=1
- flask run

Docs:
- https://docs.mongoengine.org/guide/defining-documents.html

Local container:
- docker run -p 27017:27017 --mount source=moviestr_authent,target=/app mongo