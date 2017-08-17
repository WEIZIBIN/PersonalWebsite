from flask import Blueprint, redirect, url_for

general = Blueprint('general', __name__)


@general.route('/')
def index():
    return redirect(url_for('chat.index'))
