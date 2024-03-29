from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import login_required
from flask_security import current_user

from beebloge import db
from beebloge.comments.forms import CommentForm
from beebloge.models import Comment, Product
from beebloge.products.forms import ProductForm
from beebloge.users.picture_handler import add_pic, del_pic
from beebloge.users.views import requires_roles
import urllib.parse

products = Blueprint('products', __name__)


@products.route('/create/product', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def create_product():
    form = ProductForm()

    if form.validate_on_submit() and form.check_title():

        if form.picture.data:
            imgname = "".join([form.title.data[:20], form.category.data])
            pic = add_pic(form.picture.data, imgname, 'product_pics', (450, 600))

            Product(title           =form.title.data,
                    text            =form.text.data,
                    short_text      =form.shortText.data,
                    category        =form.category.data,
                    user_id         =current_user.id,
                    product_image   =pic)

            flash("Blog Post Created")
            return redirect(url_for('core.index'))

    return render_template('addProduct.html', form=form)


@products.route('/product/<int:product_id>', strict_slashes=False, methods=["GET", "POST"])
def product(product_id):
    # grab the requested blog post by id number or return 404
    product = Product.query.get_or_404(product_id)
    form = CommentForm()
    if form.validate_on_submit():
        Comment(body        =form.comment.data,
                post_id     ='',
                product_id  =product.id,
                user_id     =current_user.id)

        # flash("Your comments has been added to the post", "success")

    return render_template('product.html',
                           title        =product.title,
                           date         =product.date,
                           product      =product,
                           category     =product.category,
                           product_image=product.product_image,
                           form         =form)


@products.route('/product/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update(product_id):
    product = Product.query.get_or_404(product_id)
    if product.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = ProductForm()

    if form.validate_on_submit():
        if form.picture.data:
            imgname = "".join([form.title.data[:20], form.category.data])
            del_pic(fileName=product.product_image)
            pic = add_pic(form.picture.data, imgname, 'product_pics', (450, 600))
            product.post_image = pic

        product.title       = form.title.data
        product.text        = form.text.data
        product.category    = form.category.data
        product.short_text  = form.shortText.data

        db.session.commit()
        # flash('Post Updated')
        return redirect(url_for('products.products_list', product_id=product.id))
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data     = product.title
        form.text.data      = product.text
        form.shortText.data = product.short_text
        form.category.data  = product.category
        form.picture.data   = product.product_image

    return render_template('addProduct.html', title='Update',
                           form=form)


@products.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.author != current_user:
        abort(403)
    del_pic(fileName=product.product_image)
    db.session.delete(product)
    db.session.commit()
    # flash('Post has been deleted')
    return redirect(url_for('products.products_list'))


@products.route('/product/list')
def products_list():
    '''
    This is the home page view. Use pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    categories = Product.get_category_list()
    products = Product.get_products_list()

    return render_template('productList.html', products=products, categories=categories)


@products.route('/product/list/filter/<string:query>', methods=['POST', 'GET'])
def products_list_filter(query):
    categories = Product.get_category_list()
    products = Product.find_by_category(urllib.parse.unquote(query))
    return render_template('productList.html', products=products, categories=categories)
