from flask_website.views import chat
from flask_website.views import general
from flask import Flask

app = Flask(__name__)

app.register_blueprint(chat)
app.register_blueprint(general)