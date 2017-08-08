from flask import Flask, render_template, jsonify, request
from weibo import init_xiaoice

app = Flask(__name__)
xiaoice = init_xiaoice()


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/message', methods=['POST'])
def message():
    post_data = request.get_json()
    msg = post_data['msg']
    xiaoice.post_msg_to_xiaoice(msg)
    return jsonify(retCode='0')


@app.route('/im', methods=['POST'])
def im():
    post_data = request.get_json()
    msg = xiaoice.get_msg_from_xiaoice()
    return jsonify(retCode='0', msg=msg)


if __name__ == '__main__':
    app.run()
