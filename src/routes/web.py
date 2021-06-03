from flask import Blueprint, render_template

web = Blueprint("web", __name__)


@web.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@web.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
