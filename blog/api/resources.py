from flask_restful import Resource, reqparse
from blog.models import Post
from blog import db

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
        args = parser.parse_args()
        post = Post.query.get_or_404(post_id)
        post.title = args['title']
        post.content = args['content']
        db.session.commit()
        return {'message': 'Blog post updated successfully'}

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Blog post deleted successfully'}

# Resource for handling all blog posts
class BlogPostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return [{'title': post.title, 'content': post.content} for post in posts]

    def post(self):
        args = post_parser.parse_args()
        post = Post(title=args['title'], content=args['content'])
        db.session.add(post)
        db.session.commit()
        return {'message': 'Post created successfully'}, 201

