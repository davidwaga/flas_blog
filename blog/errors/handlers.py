from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(e):
    return render_template('error.html', error_num=404, error_text=' The page you’re looking for doesn’t exist.'), 404


@errors.app_errorhandler(403)
def error_403(e):
    return render_template('error.html', error_num=403, error_text='Please check your account and try again.'), 403


@errors.app_errorhandler(500)
def error_500(e):
    return render_template('error.html', error_num=500, error_text="We're experiencing some trouble on our end. "
                                                                   "Please try again in the near future."), 500