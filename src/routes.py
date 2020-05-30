from flask import Blueprint, render_template

main = Blueprint(__name__, "routes")


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')
