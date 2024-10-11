from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from app.auth import auth
from app.models import User
from app import db
from app.auth.forms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('post.post_list'))
    return render_template('users/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data,)
        user.set_password(form.password.data)  # Hash the password using your model's method
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('users/register.html', form=form)



