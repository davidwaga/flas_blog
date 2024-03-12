from flask_restful import Resource, reqparse
from blog.models import Post
from blog import db
from flask import request
# Define parsers for request data
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, help='Title of the post')
post_parser.add_argument('content', type=str, help='Content of the post')
# Resource for handling individual blog posts
class BlogPostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return {'title': post.title, 'content': post.content}

    def put(self, post_id):
        data = request.json
        post = Post.query.get_or_404(post_id)
        post.title = data['title']
        post.content = data['content']
        post.user_id = data['user_id']
        db.session.commit()
        return {'message': 'Post updated successfully'}

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted successfully'}

# Resource for handling all blog posts
class BlogPostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return [{'title': post.title, 'content': post.content} for post in posts]

    def post(self):
        data = request.json
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return {'message': 'Post created successfully'}, 201

