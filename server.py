from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/xiaoice', methods=['POST'])
def xiaoice():
    return jsonify(retCode='0')


@app.route('/im', methods=['POST'])
def im():
    return jsonify(retCode='0', msg='helloworld')


if __name__ == '__main__':
    app.run()
