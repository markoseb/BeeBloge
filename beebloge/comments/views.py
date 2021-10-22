from flask import url_for,redirect,Blueprint,abort
from flask_login import login_required
from flask_security import current_user
from beebloge import db
from beebloge.models import BlogPost,Comment,Product

comments = Blueprint('comments',__name__)


@comments.route('/<int:postProductId>/delete/<int:comment_id>/', methods=[ "POST"])
@login_required
def delete_comment(postProductId,comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.author == current_user or current_user.has_role('admin'):
        db.session.delete(comment)
        db.session.commit()
        # flash('Comment has been deleted')
        if comment.post_id:
            blog_post = BlogPost.query.get_or_404(postProductId)
            return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
        if comment.product_id:
            product = Product.query.get_or_404(postProductId)
            return redirect(url_for('products.product', product_id=product.id))
    else:
        abort(403)



