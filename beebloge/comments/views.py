from flask import url_for,redirect,Blueprint
from flask_login import login_required
from flask_security import current_user
from beebloge import db
from beebloge.models import BlogPost,Comment,Product

comments = Blueprint('comments',__name__)


@comments.route('/<int:product_id>/<int:blog_post_id>/delete/<int:comment_id>/', methods=[ "POST"])
@login_required
def delete_comment(product_id,blog_post_id,comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.author == current_user or current_user.has_role('admin'):
        db.session.delete(comment)
        db.session.commit()
        # flash('Comment has been deleted')
        if blog_post_id:
            blog_post = BlogPost.query.get_or_404(blog_post_id)
            return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
        if product_id:
            product = Product.query.get_or_404(blog_post_id)
            return redirect(url_for('products.products', product_id=product.id))
    else:
        abort(403)



