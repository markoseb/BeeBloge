from beebloge import db,app
from beebloge.models import User,Role
from beebloge.users.views import MyModelView,MyAdminIndexView
from flask_security import Security
from beebloge.users.views import user_datastore
from flask_admin import Admin

admin=Admin(index_view=MyAdminIndexView(User,db.session))
admin.init_app(app) # This line is new
admin.add_view(MyModelView(User,db.session))

security =Security(app,user_datastore)