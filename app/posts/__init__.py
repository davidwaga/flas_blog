from flask import Blueprint

post = Blueprint('post', __name__, template_folder='templates')

from app.posts import routes
