from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import db
from app.models import CartItem, Product, Order, OrderItem

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.subtotal() for item in items)
    return render_template('cart.html', items=items, total=total)


@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    existing = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if existing:
        existing.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id)
        db.session.add(item)

    db.session.commit()
    flash(f'"{product.name}" added to cart!', 'success')
    return redirect(url_for('orders.products')) 


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash('Not allowed.', 'danger')
        return redirect(url_for('cart.view_cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Item removed.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/update/<int:item_id>/<action>', methods=['POST'])
@login_required
def update_quantity(item_id, action):
    item = CartItem.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash('Not allowed.', 'danger')
        return redirect(url_for('cart.view_cart'))

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
        else:
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('cart.view_cart'))

    db.session.commit()
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart.view_cart'))

    total = sum(item.subtotal() for item in items)

  
    from app.models import Customer
    customer = Customer.query.filter_by(email=current_user.email).first()
    if not customer:
        customer = Customer(name=current_user.name, email=current_user.email)
        db.session.add(customer)
        db.session.flush()

    order = Order(
        customer_id=customer.id,
        product_id=items[0].product_id, 
        quantity=sum(i.quantity for i in items),
        total_price=total
    )
    db.session.add(order)
    db.session.flush()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=item.product.price
        )
        db.session.add(order_item)
        db.session.delete(item)  # clear cart

    db.session.commit()
    flash(f'🎉 Order #{order.id} placed successfully!', 'success')
    return redirect(url_for('orders.orders')) 