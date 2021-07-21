from beebloge import db,admin,app
from beebloge.models import User
from beebloge.users.views import MyModelView
from flask_security import Security
from beebloge.users.views import user_datastore

admin.add_view(MyModelView(User,db.session))
security =Security(app,user_datastore)