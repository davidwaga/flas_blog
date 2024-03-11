from flask import Blueprint
from flask_restful import Api
from blog.api.resources import BlogPostListResource, BlogPostResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Define API endpoints
api.add_resource(BlogPostListResource, '/blogs')
api.add_resource(BlogPostResource, '/blogs/<int:post_id>')
