from flask import Blueprint, jsonify, request
from blog.models import Post
from blog import db
from flask_restful import Api, Resource, reqparse

api = Blueprint('api', __name__)

# Define parsers for request data
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('content')


# # Routes for posts
# @api.route('/posts', methods=['GET'])
# def get_posts():
#     posts = Post.query.all()
#     return jsonify([{'title': post.title, 'content': post.content} for post in posts])

@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({'title': post.title, 'content': post.content})

@api.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        posts = Post.query.all()
        return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])
    elif request.method == 'POST':
        data = request.json
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        if title and content:
            new_post = Post(title=title, content=content, user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            return jsonify({'message': 'Post created successfully'}), 201
        else:
            return jsonify({'error': 'Missing title or content'}), 400

@api.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        return jsonify({'id': post.id, 'title': post.title, 'content': post.content})
    elif request.method == 'PUT':
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if title and content:
            post.title = title
            post.content = content
            db.session.commit()
            return jsonify({'message': 'Post updated successfully'})
        else:
            return jsonify({'error': 'Missing title or content'}), 400
    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()

# @api.route('/posts', methods=['POST'])
# def create_post():
#     data = request.json
#     if isinstance(data, dict):  # Check if data is a dictionary
#         title = data.get('title')
#         content = data.get('content')

#         if title and content:
#             new_post = Post(title=title, content=content)
#             jsonify(new_post)
#             db.session.add(new_post)
#             db.session.commit()
#             return jsonify({'message': 'Post created successfully'}), 201
#         else:
#             return jsonify({'error': 'Title and content are required'}), 400
#     else:
#         return jsonify({'error': 'Invalid JSON data'}), 400


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
