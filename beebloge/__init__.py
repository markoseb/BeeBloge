import os
from flask import Flask,request,send_from_directory,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_ckeditor import  CKEditor,upload_success, upload_fail

app = Flask(__name__)
Bootstrap(app)
#############################################################################
############ CONFIGURATIONS ###############
###########################################################################

# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CKEDITOR_SERVE_LOCAL'] = False
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/upload_img/')


db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################


from beebloge.core.views import core
from beebloge.users.views import users
from beebloge.blog_posts.views import blog_posts
from beebloge.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)







@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/static/upload_img'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('/static/upload_img', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call