from flask import Blueprint, render_template

view = Blueprint("view", __name__)


@view.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@view.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
