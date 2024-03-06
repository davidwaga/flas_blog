from api.api_blueprint import bp
from flask import Flask, Blueprint, jsonify
from werkzeug.exceptions import abort
from database.db import get_db_connection
from flask_restful import Resource, Api
from datetime import datetime
import json
@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    #post = [tuple(row) for row in post]
    return post


@bp.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    #convert row tuples to serializable tuples
    posts = [tuple(row) for row in posts]
    return jsonify(posts)

@bp.route("/posts", methods=['POST'])
def create_post():
    data = request.json
    post_success = post_blog_handler(data["title"], data["content"])
    
    if post_success:
        return Response({'success: true'}, status = 200)
    return Response({'success: false'}, status = 500)
# @bp.route('/posts/<int:id>', methods=['PUT'])
# def update_post(id):
#     pass


@bp.route('/posts/<int:id>', methods=['DELETE'])
def update_post(id):
    pass
