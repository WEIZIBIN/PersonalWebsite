from flask_website import app, login_manager
from flask_website.views import chat, general, admin, xiaoice
from flask_website.config import secret_key, session_type
import logging.config

app.register_blueprint(chat)
app.register_blueprint(general)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(xiaoice, url_prefix='/admin/xiaoice')

if __name__ == '__main__':
    logging.config.fileConfig('log.conf')
    login_manager.init_app(app)
    app.secret_key = secret_key
    app.config['SESSION_TYPE'] = session_type
    app.run(threaded=True, debug=True)
