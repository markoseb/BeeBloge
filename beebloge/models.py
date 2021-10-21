from beebloge import db,login_manager
from datetime import datetime
from flask_security import RoleMixin,UserMixin
from beebloge.utils import verify_password


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create a table of users and user roles
roles_users_table = db.Table('roles_users',
                            db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                            db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    products = db.relationship('Product', backref='author', lazy=True)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=roles_users_table, backref=db.backref('users'), lazy='dynamic')




    def check_password(self, password):
        return verify_password(password, self.password)

    def __repr__(self):
        return f"UserName: {self.username} roles: {self.roles[0]}"



class Role(db.Model,RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

  def __init__(self, id, name, description):
      self.id = id
      self.name = name
      self.description = description



class BlogPost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User,overlaps="author,posts")

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_image = db.Column(db.String(140), nullable=False, default='static/post_pics/blog-1.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref=db.backref('blog_post'), lazy='dynamic')

    def __init__(self, title, text, user_id,post_image,category="Category" ):
        self.title = title
        self.text = text
        self.category = category
        self.user_id =user_id
        self.post_image=post_image


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"

class Comment(db.Model):
    users = db.relationship(User,overlaps="author,comments")

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_id = db.Column('post_id',db.Integer, db.ForeignKey('blog_post.id'),nullable=True)
    product_id = db.Column('product_id',db.Integer, db.ForeignKey('product.id'),nullable=True)

    def __init__(self, body, post_id,user_id,product_id):
        self.body = body
        self.post_id = post_id
        self.product_id = product_id
        self.user_id = user_id

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"


class Product(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User, overlaps="author,products")
    # Model for the Product on Website
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_image = db.Column(db.String(140), nullable=False, default='static/product_pics/blog-1.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref=db.backref('product'), lazy='dynamic')

    def __init__(self, title, text, product_image,user_id,category="Category" ):
        self.title = title
        self.text = text
        self.category = category
        self.product_image=product_image
        self.user_id = user_id


    def __repr__(self):
        return f"Product Id: {self.id} --- Date: {self.date} --- Title: {self.title}"