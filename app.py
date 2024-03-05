import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from posts.posts_blueprint import posts_blueprint
#from auth.auth_blueprint import auth_blueprint
from api.api_blueprint import bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


app.register_blueprint(posts_blueprint, url_prefix='/')
#app.register_blueprint(users_blueprint, url_prefix='/auth')


app.register_blueprint(bp, url_prefix='/api/v1')


# route for "/about"
@app.route('/about')
def about():
    return 'This is the about page'



if __name__ == '__main__':
    app.run(debug=True)
