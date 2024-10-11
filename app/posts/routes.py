from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.posts import post
from app.models import Post, Comment
from app.posts.forms import PostForm, CommentForm
from app import db

@post.route('/')
@login_required
def post_list():
    posts = Post.query.filter_by(author_id=current_user.id).all()
    return render_template('posts/post_list.html', posts=posts)

@post.route('/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', post=post)


@post.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        comment = Comment(content=form.content.data, post_id=post.id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post.post_detail', post_id=post.id))
    return redirect(url_for('post.post_detail', post_id=post_id))

@post.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.post_list'))
    return render_template('posts/post_form.html', form=form)

@post.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post.post_list'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/post_form.html', form=form)

@post.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post.post_list'))
