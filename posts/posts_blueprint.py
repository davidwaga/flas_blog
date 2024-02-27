from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from db.db import get_db_connection
posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')

#get all posts
@posts_blueprint.route('/')
def post_list():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts/post_list.html', posts=posts)

#get single post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

#get a specific post
@posts_blueprint.route('/posts/<int:post_id>')
def post_detail(post_id):
    post = get_post(post_id)
    return render_template('posts/post_detail.html', post=post)

# function to create a post
@posts_blueprint.route('/posts/create', methods=('GET', 'POST'))
def post_create():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('posts_blueprint.post_list'))
    return render_template('posts/create_post.html')

#function to edit post
@posts_blueprint.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
def post_edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('posts_blueprint.post_list'))

    return render_template('posts/edit_post.html', post=post)


# function to delete post
@posts_blueprint.route('/posts/<int:id>/delete', methods=('POST',))
def post_delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('posts_blueprint.post_list'))

