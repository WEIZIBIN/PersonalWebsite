import time
from threading import Timer

from flask import Blueprint, render_template, request, jsonify, session

from flask_website.config import disconnect_after_not_post_back
from flask_website.im import xiaoice_storage

chat = Blueprint('chat', __name__)

last_im_time = {}


@chat.route('/index')
def index():
    return render_template('chat.html')


@chat.route('/handshake', methods=['POST'])
def handshake():

    # second request
    if 'client_id' in session:
        return jsonify(retCode='1', msg='Hello, I am here!')

    # first request
    client_id = xiaoice_storage.get_avail_xiaoice_client_id()
    if client_id is not None:
        session['client_id'] = client_id
        return jsonify(retCode='0', msg='Hello, I am xiaoice!')

    return jsonify(retCode='-1', msg='Xiaoice is busy!')


@chat.route('/message', methods=['POST'])
def message():
    post_data = request.get_json()
    msg = post_data['msg']
    xiaoice = xiaoice_storage.get_xiaoice_by_client_id(session['client_id'])
    xiaoice.send_msg(msg)
    return jsonify(retCode='0', msg=msg)


@chat.route('/im', methods=['POST'])
def im():

    client_id = session['client_id']
    last_im_time[client_id] = time.time()
    xiaoice = xiaoice_storage.get_xiaoice_by_client_id(session['client_id'])

    msg = xiaoice.get_msg()

    timer = Timer(disconnect_after_not_post_back, check_im_alive, args=(client_id,))
    timer.start()

    return jsonify(retCode='0', msg=msg)


def check_im_alive(client_id):
    last_connect_time = last_im_time[client_id]
    now = time.time()
    if now - last_connect_time > disconnect_after_not_post_back:
        del last_im_time[client_id]
        xiaoice_storage.free_xiaoice_by_client_id(client_id)
