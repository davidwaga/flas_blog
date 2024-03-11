from flask import Blueprint, jsonify, request
from blog.models import Post
from blog import db, app
from flask_restful import Api, Resource, reqparse

api = Blueprint('api', __name__)

# Define parsers for request data
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('content')


# Routes for posts
@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'title': post.title, 'content': post.content} for post in posts])

@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({'title': post.title, 'content': post.content})


@api.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    if isinstance(data, dict):  # Check if data is a dictionary
        title = data.get('title')
        content = data.get('content')

        if title and content:
            new_post = Post(title=title, content=content)
            jsonify(new_post)
            db.session.add(new_post)
            db.session.commit()
            return jsonify({'message': 'Post created successfully'}), 201
        else:
            return jsonify({'error': 'Title and content are required'}), 400
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400


@api.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.json
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})


@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})

#routes for users


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass


@api.route('/users', methods=['GET'])
def get_users():
    pass


@api.route('/users', methods=['POST'])
def create_user():
    pass


@api.route('/users/<int:id>/', methods=['PUT'])
def update_user(id):
    pass


# Resource for handling individual blog posts
class BlogPostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return {'title': post.title, 'content': post.content}

    def put(self, post_id):
        args = parser.parse_args()
        post = Post.query.get_or_404(post_id)
        post.title = args['title']
        post.content = args['content']
        db.session.commit()
        return {'message': 'Blog post updated successfully'}

    def delete(self, post_id):
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Blog post deleted successfully'}

# Resource for handling all blog posts
class BlogPostListResource(Resource):
    def get(self):
        posts = BlogPost.query.all()
        return [{'title': post.title, 'content': post.content} for post in posts]

    def post(self):
        args = parser.parse_args()
        new_post = Post(title=args['title'], content=args['content'])
        db.session.add(new_post)
        db.session.commit()
        return {'message': 'Blog post created successfully'}, 201



