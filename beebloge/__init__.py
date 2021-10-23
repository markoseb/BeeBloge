import os
from flask import Flask, Response, send_from_directory, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
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
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'sha256'

db = SQLAlchemy(app)

Migrate(app, db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"
login_manager.session_protection = 'strong'

###########################
#### BLUEPRINT CONFIGS #######
#########################


from beebloge.core.views import core
from beebloge.users.views import users
from beebloge.blogPosts.views import blog_posts
from beebloge.error_pages.handlers import error_pages
from beebloge.comments.views import comments
from beebloge.products.views import products

# Register the apps
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(comments)
app.register_blueprint(products)

@app.before_request
def redirect_nonwww():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == 'roztanczonapszczolka.pl':

        urlparts_list = list(urlparts)
        urlparts_list[1] = "www.roztanczonapszczolka.pl"
        urlparts_list[0] = "https"
        return redirect(urlunparse(urlparts_list), code=301)



@app.route('/robots.txt')
def robots():
    r = Response(response="User-Agent: *\nDisallow: /*.sqlite$\nSitemap: https://roztanczonapszczolka.pl/sitemap.xml\n",
                 status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

















