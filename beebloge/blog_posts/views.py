from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import login_required
from flask_security import current_user
from beebloge import db
from beebloge.models import BlogPost,Comment
from beebloge.users.picture_handler import add_pic
from beebloge.users.views import requires_roles
from beebloge.blog_posts.forms import BlogPostForm
from beebloge.comments.forms import CommentForm
blog_posts = Blueprint('blog_posts',__name__)

@blog_posts.route('/create',methods=['GET','POST'])
@login_required
@requires_roles('admin')
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        if form.picture.data:
            imgname = "".join([form.title.data[:10], form.category.data])
            pic = add_pic(form.picture.data, imgname, 'post_pics',(600,600))

            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             category=form.category.data,
                             user_id=current_user.id,
                             post_image=pic)


            db.session.add(blog_post)
            db.session.commit()
        # flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)



@blog_posts.route('/<int:blog_post_id>', methods=["GET", "POST"])
def blog_post(blog_post_id):
    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data, post_id=blog_post.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        # flash("Your comments has been added to the post", "success")

    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post,category=blog_post.category,post_image=blog_post.post_image,form=form
    )

@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = BlogPostForm()
    if form.picture.data:
        imgname = "".join([form.title.data, form.category.data])
        pic = add_pic(form.picture.data, imgname, 'post_pics', (800, 800))
        blog_post.post_image = pic
    if form.validate_on_submit() :
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        blog_post.category = form.category.data

        db.session.commit()
        # flash('Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
        form.category.data = blog_post.category
        form.picture.data =blog_post.post_image

    return render_template('create_post.html', title='Update',
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    # flash('Post has been deleted')
    return redirect(url_for('core.index'))






