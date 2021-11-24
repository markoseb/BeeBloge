from flask import render_template, Blueprint
from flask_security import current_user
from beebloge import db
from beebloge.messages.forms import MessageForm

messages = Blueprint('messages',__name__)

@messages.route('/create/message', methods = ['GET','POST'])
def create_message():
    form = MessageForm()

    if current_user.is_active and current_user.is_authenticated:
        form.email.data = current_user.email
        form.firstName.data = current_user.name

    return render_template('contact.html',form = form)
