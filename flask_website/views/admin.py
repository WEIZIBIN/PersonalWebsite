from flask import Blueprint, request, render_template
from flask_login import login_user, login_required
from flask_website.user import User
from flask_website import login_manager

admin = Blueprint('admin', __name__)


@admin.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        user = User('1', username, password)
        if login_user(user):
            return 'login success:' + username

    return render_template('admin/login.html')


@admin.route('/index')
@login_required
def index():
    return render_template('admin/index.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    # todo
    pass

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)
