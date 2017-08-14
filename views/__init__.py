from flask import Flask

from views.chat import chat
from views.general import general


app = Flask(__name__)

app.register_blueprint(chat, url_prefix='/chat')
app.register_blueprint(general, url_prefix='/')
