from flask import Blueprint, request
from mongoengine.context_managers import switch_collection
from .models import Movie

main = Blueprint(__name__, "routes")


@main.route('/')
def index():
    return "Backend Up"


@main.route('/movie', methods=['POST'])
def post_movie():
    obj = request.get_json()
    try:
        name = obj["name"]
    except:
        abort(400, "No name given")
    movie = Movie.objects(name=name).first()
    if not movie:
        new_movie = Movie(**obj) 
        new_movie.save()
        return "Success", 200
    return "Failed", 400