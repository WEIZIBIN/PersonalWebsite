from views import app
import logging.config

if __name__ == '__main__':
    logging.config.fileConfig('log.conf')
    app.run(threaded=True)
