import sqlite3
from flask import Flask, request
from werkzeug.exceptions import abort
from posts.posts_blueprint import posts_blueprint
#from auth.auth_blueprint import auth_blueprint
from api.api_blueprint import bp
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)

app.register_blueprint(posts_blueprint, url_prefix='/')
#app.register_blueprint(users_blueprint, url_prefix='/auth')
#app.add_api("swagger.yml")

#database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


app.register_blueprint(bp, url_prefix='/api/v1')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime,  default=db.func.current_timestamp())

    def __repr__(self):
        return self.title


fakeDatabase = {
    1:{'title':'Blog 1','content':'What is new in blog 1'},
    2:{'title':'Blog 2','content':'What is new in blog 2'},
    3:{'title':'Blog 3','content':'What is new in blog 3'},
}

postFields = {
    'id':fields.Integer,
    'title':fields.String,
    'content':fields.String,
    'created': fields.DateTime
}
class Posts(Resource):
    @marshal_with(postFields)
    def get(self):
        posts = Post.query.all()
        return posts

    @marshal_with(postFields)
    def post(self):
        data = request.json
        post = Post(title=data['title'],content=data['content'])
        db.session.add(post)
        db.session.commit()

        posts = Post.query.all()
        # itemId = len(fakeDatabase.keys()) + 1
        # fakeDatabase[itemId] = {'name':data['name']}
        return posts


class Post(Resource):
    @marshal_with(postFields)
    def get(self, pk):
        post = Post.query.filter_by(id=pk).first()
        return post

    @marshal_with(postFields)
    def put(self, pk):
        data = request.json
        post = Post.query.filter_by(id=pk).first()
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        #fakeDatabase[pk]['name'] = data['name']
        return post

    @marshal_with(postFields)
    def delete(self, pk):
        post = Post.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        posts = Post.query.all()
        #del fakeDatabase[pk]
        return posts

api.add_resource(Posts, '/api/v1/posts')
api.add_resource(Post, '/api/v1/posts/<int:pk>')


# route for "/about"
@app.route('/about')
def about():
    return 'This is the about page'



if __name__ == '__main__':
    app.run(debug=True)
