from flask_website import app, login_manager
from flask_website.config import secret_key

from flask_website.views.admin import admin
from flask_website.views.xiaoice import xiaoice
from flask_website.views.general import general
from flask_website.views.chat import chat

import logging.config
from os import path

logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), 'log.conf'))

app.register_blueprint(chat)
app.register_blueprint(general)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(xiaoice, url_prefix='/admin/xiaoice')

login_manager.init_app(app)
app.secret_key = secret_key

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
