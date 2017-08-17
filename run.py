from flask_website import app, login_manager
import logging.config

if __name__ == '__main__':
    logging.config.fileConfig('log.conf')
    login_manager.init_app(app)
    app.run(threaded=True)
