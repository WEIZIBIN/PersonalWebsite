from flask import Blueprint, render_template, request
from flask_login import login_required

xiaoice = Blueprint('xiaoice', __name__)


@xiaoice.route('/index')
@login_required
def index():
    return render_template('admin/xiaoice/index.html')


@xiaoice.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('admin/xiaoice/add.html')
    if request.method == 'POST':
        pass
