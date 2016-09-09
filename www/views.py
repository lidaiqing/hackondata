from flask import render_template, Blueprint

views_bp = Blueprint(
    'views',
    __name__)

@views_bp.route('/')
def show_maps():
    return render_template('index.html')
