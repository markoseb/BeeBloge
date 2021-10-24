from flask import render_template,request,Blueprint,redirect
from beebloge.models import BlogPost

core = Blueprint('core',__name__)


@core.route('/index')
def indexRedirect():
  return redirect('/')


@core.route('/')
def index():
    '''
    This is the home page view. Use pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',blog_posts=blog_posts)




@core.route('/info')
def info():
    '''
    Example view of any other "core" page.
    '''
    return render_template('info.html')
