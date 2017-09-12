import logging
from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required
from threading import Thread
from flask_website import xiaoice_storage
from flask_website.weibo import init_xiaoice, init_xiaoice_with_captcha

xiaoice = Blueprint('xiaoice', __name__)

logger = logging.getLogger('admin.xiaoice')

@xiaoice.route('/index')
@login_required
def index():
    return render_template('admin/xiaoice/index.html', dict_xiaoice=xiaoice_storage.get_all_xiaoice())


@xiaoice.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('admin/xiaoice/add.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Thread(target=_handle_add_xiaoice(username, password)).start()
        return redirect(url_for('xiaoice.index'))


@xiaoice.route('/get_captcha', methods=['GET'])
@login_required
def get_captcha():
    username = request.args.get('username')
    xiaoice = xiaoice_storage.get_xiaoice_by_username(username)
    if not xiaoice.is_login and xiaoice.need_captcha:
        return render_template('admin/xiaoice/captcha_dialog.html', username=username)


@xiaoice.route('/show_captcha', methods=['GET'])
@login_required
def show_captcha():
    username = request.args.get('username')
    xiaoice = xiaoice_storage.get_xiaoice_by_username(username)
    return Response(xiaoice.get_captcha(), mimetype='image/jpeg')


@xiaoice.route('/input_captcha', methods=['POST'])
@login_required
def input_captcha():
    username = request.form['username']
    captcha = request.form['captcha']
    Thread(target=_handle_input_captcha(username, captcha)).start()
    return redirect(url_for('xiaoice.index'))


def _handle_input_captcha(username, captcha):
    xiaoice = xiaoice_storage.get_xiaoice_by_username(username)
    init_xiaoice_with_captcha(xiaoice, captcha)


def _handle_add_xiaoice(username, password):
    xiaoice = init_xiaoice(username, password)
    logger.debug('add %s to xiaoice storage' % xiaoice)
    xiaoice_storage.add_xiaoice(xiaoice)
