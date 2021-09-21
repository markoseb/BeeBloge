from flask import render_template, url_for, flash, redirect, request, Blueprint,abort
from flask_login import login_user, logout_user, login_required
from beebloge import db
from beebloge.models import User, BlogPost,Role
from beebloge.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from beebloge.users.picture_handler import add_pic
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView,expose
from functools import wraps
from flask_security import SQLAlchemySessionUserDatastore,current_user
from flask_security.utils import hash_password

user_datastore=SQLAlchemySessionUserDatastore(db.session,User,Role)
users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit()  and form.check_email() and form.check_username():

        role = user_datastore.find_or_create_role(name='user', description='FOLLOW | COMMENT')

        user = user_datastore.create_user(email=form.email.data,
                                          first_name=form.username.data,
                                          password=hash_password(form.password.data))

        user_datastore.add_role_to_user(user, role)
        db.session.commit()

        # flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = user_datastore.get_user(form.email.data)
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Jesteś zalogowany!')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
        else:
            flash('Błędne hasło!')

    return render_template('security\login_user.html', login_user_form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        current_user.first_name = form.username.data
        current_user.email = form.email.data
        user = user_datastore.get_user(current_user.email)
        user.password=hash_password(form.password.data)
        if form.picture.data :
            username = current_user.first_name
            pic = add_pic(form.picture.data, username,'profile_pics',(800,800))
            current_user.profile_image = pic
        db.session.commit()

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.first_name
        form.email.data = current_user.email


    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(first_name=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
# </editor-fold>


# Create a ModelView to add to our administrative interface
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated :
            return redirect(url_for('/login'))
        return super(MyAdminIndexView, self).index()

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and  current_user.has_role('admin'))
    def _handle_view(self, name):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            return redirect(url_for('users.login'))

# Create a ModelView to add to our administrative interface
class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and current_user.has_role('admin'))

    def _handle_view(self, name):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            return redirect(url_for('users.login'))

    column_list = ['email', 'password']





def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            for role in roles:
                if current_user.has_role(role):
                    # Redirect the user to an unauthorized notice!
                    return f(*args, **kwargs)

            return "You are not authorized to access this page"
        return wrapped
    return wrapper