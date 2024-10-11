from flask import Flask
from app.extends import db, migrate, login_manager
from flask_restful import Api
from app.api.resources import UserAPI, PostAPI, CommentAPI, api
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db
    api.init_app(app)
    #api = Api(app)

    from app.auth import auth as auth_blueprint
    from app.posts import post as posts_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(posts_blueprint, url_prefix='/posts')

    # Register APIs
    api.add_resource(UserAPI, '/api/v1/users/<int:user_id>')
    api.add_resource(PostAPI, '/api/v1/posts', '/api/posts/<int:post_id>')
    api.add_resource(CommentAPI, '/api/v1/comments', '/api/comments/<int:comment_id>')
    
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
