from flask_restful import Resource, reqparse
from app.models import User, Post, Comment

# Parser for creating/updating posts
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', required=True)
post_parser.add_argument('content', required=True)
post_parser.add_argument('user_id', type=int, required=True)

# User API
class UserAPI(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username,}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}

# Post API
class PostAPI(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return {'id': post.id, 'title': post.title, 'content': post.content, 'user_id': post.user_id}

    def post(self):
        args = post_parser.parse_args()
        post = Post(title=args['title'], content=args['content'], user_id=args['user_id'])
        db.session.add(post)
        db.session.commit()
        return {'message': 'Post created', 'post_id': post.id}

    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        args = post_parser.parse_args()
        post.title = args['title']
        post.content = args['content']
        db.session.commit()
        return {'message': 'Post updated'}

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {'message': 'Post deleted'}

# Comment API
class CommentAPI(Resource):
    def get(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        return {'id': comment.id, 'content': comment.content, 'post_id': comment.post_id, 'user_id': comment.user_id}

    def post(self):
        args = reqparse.RequestParser()
        args.add_argument('content', required=True)
        args.add_argument('post_id', type=int, required=True)
        args.add_argument('user_id', type=int, required=True)
        args = args.parse_args()
        comment = Comment(content=args['content'], post_id=args['post_id'], user_id=args['user_id'])
        db.session.add(comment)
        db.session.commit()
        return {'message': 'Comment created', 'comment_id': comment.id}

    def delete(self, comment_id):
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted'}



class UserAPI(Resource):
    """
    User API
    GET: Retrieve a user by ID.
    DELETE: Delete a user by ID.
    """
    def get(self, user_id):
        """
        Retrieve a user by ID.
        ---
        parameters:
          - in: path
            name: user_id
            required: true
            schema:
              type: integer
            description: The user ID
        responses:
          200:
            description: A user object
        """
        user = User.query.get_or_404(user_id)
        return {'id': user.id, 'username': user.username, 'email': user.email}
