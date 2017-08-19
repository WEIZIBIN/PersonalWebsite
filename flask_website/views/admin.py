from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_user, login_required
from flask_website.user import User
from flask_website import login_manager
from flask_website.config import admin_id, admin_username,admin_password

admin = Blueprint('admin', __name__)


@admin.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            user = User(admin_id, admin_username, admin_password)
            if login_user(user):
                return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password!', category='danger')
    return render_template('admin/login.html')


@admin.route('/index')
@login_required
def index():
    return render_template('admin/index.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Please login first!', category='danger')
    return redirect(url_for('admin.login'))


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)
