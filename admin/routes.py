
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)

from flask_login import login_required, current_user
from functools import wraps

from app import db
from app.models import Product, Order, User
from app.forms import ProductForm
from app.models import ContactMessage

admin_bp = Blueprint('admin', __name__)


# =========================
# ADMIN DECORATOR (FIXED)
# =========================
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)

        if not current_user.is_admin:
            abort(403)

        return func(*args, **kwargs)

    return wrapper


# =========================
# ADMIN DASHBOARD
# =========================
@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():

    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()

    revenue = db.session.query(
        db.func.sum(Order.total_price)
    ).scalar() or 0

    return render_template(
        'admin_dashboard.html',
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
        revenue=revenue
    )


# =========================
# ALL PRODUCTS
# =========================
@admin_bp.route('/products')
@login_required
@admin_required
def admin_products():

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        'admin_products.html',
        products=products
    )


# =========================
# CREATE PRODUCT
# =========================
@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():

    form = ProductForm()

    if form.validate_on_submit():

        product = Product(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            description=form.description.data,
            in_stock=form.in_stock.data
        )

        db.session.add(product)
        db.session.commit()

        flash('Product created successfully!', 'success')

        return redirect(url_for('admin.admin_products'))

    return render_template(
        'product_form.html',
        form=form,
        title='Add Product'
    )


# =========================
# EDIT PRODUCT
# =========================
@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():

        product.name = form.name.data
        product.price = form.price.data
        product.category = form.category.data
        product.description = form.description.data
        product.in_stock = form.in_stock.data

        db.session.commit()

        flash('Product updated successfully!', 'success')

        return redirect(url_for('admin.admin_products'))

    return render_template(
        'product_form.html',
        form=form,
        title='Edit Product'
    )


# =========================
# DELETE PRODUCT
# =========================
@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully!', 'danger')

    return redirect(url_for('admin.admin_products'))

# ===========
# Message
# ===========

@admin_bp.route('/messages')
@login_required
@admin_required
def contact_messages():

    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()

    return render_template(
        'admin_messages.html',
        messages=messages
    )

# =============
#  STATUS
# =============

@admin_bp.route('/orders/<int:id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(id):

    order = Order.query.get_or_404(id)

    order.status = request.form.get('status')

    db.session.commit()

    flash('Order status updated successfully!', 'success')

    return redirect(url_for('orders.orders'))