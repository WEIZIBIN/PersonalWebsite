from flask import Blueprint, render_template, request, jsonify
from flask_website.weibo import init_xiaoice

chat = Blueprint('chat', __name__)
# xiaoice = init_xiaoice()


@chat.route('/index')
def index():
    print(chat.root_path)
    return render_template('chat.html')


@chat.route('/message', methods=['POST'])
def message():
    post_data = request.get_json()
    msg = post_data['msg']
    # xiaoice.post_msg_to_xiaoice(msg)
    return jsonify(retCode='0')


@chat.route('/im', methods=['POST'])
def im():
    post_data = request.get_json()
    # msg = xiaoice.get_msg_from_xiaoice()
    return jsonify(retCode='0', msg='hello')