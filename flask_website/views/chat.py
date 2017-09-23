from threading import Timer

from flask import Blueprint, render_template, request, jsonify, session
from flask_website import xiaoice_storage
from flask_website.config import disconnect_after_not_post_back
import time

chat = Blueprint('chat', __name__)

last_im_time = {}


@chat.route('/index')
def index():
    client_id = xiaoice_storage.get_avail_xiaoice_client_id()
    session['client_id'] = client_id
    return render_template('chat.html')


@chat.route('/message', methods=['POST'])
def message():
    post_data = request.get_json()
    msg = post_data['msg']
    xiaoice = xiaoice_storage.get_xiaoice_by_client_id(session['client_id'])
    xiaoice.send_msg(msg)
    return jsonify(retCode='0')


@chat.route('/im', methods=['POST'])
def im():
    client_id = session['client_id']
    last_im_time[client_id] = time.time()
    Timer(disconnect_after_not_post_back, check_im_alive, args=(client_id,)).start()
    xiaoice = xiaoice_storage.get_xiaoice_by_client_id(session['client_id'])
    msg = xiaoice.get_msg()
    return jsonify(retCode='0', msg=msg)


def check_im_alive(client_id):
    last_connect_time = last_im_time[client_id]
    now = time.time()
    if now - last_connect_time > disconnect_after_not_post_back:
        del last_im_time[client_id]
        xiaoice_storage.free_xiaoice_by_client_id(client_id)
