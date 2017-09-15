from flask import Blueprint, render_template, request, jsonify
from flask_website import xiaoice_storage

chat = Blueprint('chat', __name__)


@chat.route('/index')
def index():
    return render_template('chat.html')


@chat.route('/message', methods=['POST'])
def message():
    post_data = request.get_json()
    msg = post_data['msg']
    xiaoice = xiaoice_storage.get_avail_xiaoice()
    xiaoice.send_msg(msg)
    return jsonify(retCode='0')


@chat.route('/im', methods=['POST'])
def im():
    post_data = request.get_json()
    xiaoice = xiaoice_storage.get_avail_xiaoice()
    msg = xiaoice.get_msg()
    return jsonify(retCode='0', msg=msg)

