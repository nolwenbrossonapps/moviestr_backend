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
- docker run -p 27017:27017 --name backend_mongo -v moviestr_authent:/data/db mongo

Run a Docker container of moviestr_backend + a container for mongo, and connect them on a network for communication:

If not done, build an image for this repo:
0. docker build -t moviestr_backend .

Then:
1. docker run -p 27017:27017 --name backend_mongo -v moviestr_authent:/data/db mongo (build a mongo container with volume)
2. docker network create moviestr_network (create a bridge network)
4. docker network connect moviestr_network mongo_container_id (connect mongo container to it)
5. docker run -p 5000:5000 --name moviestr_backend moviestr_backend
6. docker network connect moviestr_network flask_container_id (connect flask container to the network)


# Next steps:

- Build the first components of Moviestr