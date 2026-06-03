from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from flask_login import current_user

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    TextAreaField,
    SubmitField,
    HiddenField
)

from wtforms.validators import (
    DataRequired,
    Email,
    NumberRange,
    Length,
    Optional,
    ValidationError
)

from app import db

from app.models import (
    Product,
    Order,
    Customer
)

import re
import time

orders_bp = Blueprint(
    'orders',
    __name__
)

# =========================
# ORDER FORM
# =========================

class OrderForm(FlaskForm):

    customer_name = StringField(
        'Customer Name',
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    customer_email = StringField(
        'Customer Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    product_id = SelectField(
        'Product',
        coerce=int,
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100)
        ]
    )

    notes = TextAreaField('Notes')

    submit = SubmitField('Place Order')

# =========================
# CONTACT FORM
# =========================

def validate_phone_number(form, field):

    if field.data:

        pattern = r'^\d{10}$'

        if not re.match(pattern, field.data):

            raise ValidationError(
                'Phone number must be exactly 10 digits'
            )

class ContactForm(FlaskForm):

    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    subject = SelectField(
        'Subject',
        choices=[
            ('General Inquiry', 'General Inquiry'),
            ('Order Issue', 'Order Issue'),
            ('Refund Request', 'Refund Request'),
            ('Feedback', 'Feedback')
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            validate_phone_number
        ]
    )

    priority = HiddenField('Priority')

    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            Length(min=20)
        ]
    )

    submit = SubmitField('Send Message')

# =========================
# RATE LIMIT STORAGE
# =========================

submission_times = []

# =========================
# HOME
# =========================

@orders_bp.route('/')
def home():

    order_count = Order.query.count()

    product_count = Product.query.count()

    customer_count = Customer.query.count()

    featured_products = Product.query.limit(6).all()

    username = None

    if current_user.is_authenticated:
        username = current_user.name

    return render_template(
        'home.html',
        username=username,
        order_count=order_count,
        product_count=product_count,
        customer_count=customer_count,
        featured_products=featured_products
    )

# =========================
# ABOUT
# =========================

@orders_bp.route('/about')
def about():

    return render_template('about.html')

# =========================
# PRODUCTS
# =========================

@orders_bp.route('/products')
def products():

    category = request.args.get('category')

    query = Product.query

    if category:
        query = query.filter_by(category=category)

    all_products = query.all()

    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template(
        'products.html',
        products=all_products,
        categories=categories,
        active_category=category
    )
# =========================
# PRODUCT DETAIL
# =========================

@orders_bp.route('/product/<int:product_id>')
def product(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        'product_detail.html',
        product=product
    )

# =========================
# ORDERS
# =========================

@orders_bp.route('/orders')
def orders():

    page = request.args.get(
        'page',
        1,
        type=int
    )

    pagination = Order.query.order_by(
        Order.id.desc()
    ).paginate(
        page=page,
        per_page=10
    )

    return render_template(
        'orders.html',
        orders=pagination.items,
        pagination=pagination
    )

# =========================
# PLACE ORDER
# =========================

@orders_bp.route('/order', methods=['GET', 'POST'])
def place_order():

    form = OrderForm()

    form.product_id.choices = [

        (p.id, p.name)

        for p in Product.query.filter_by(
            in_stock=True
        ).all()
    ]

    if form.validate_on_submit():

        customer = Customer.query.filter_by(
            email=form.customer_email.data
        ).first()

        if not customer:

            customer = Customer(
                name=form.customer_name.data,
                email=form.customer_email.data
            )

            db.session.add(customer)

            db.session.flush()

        product = Product.query.get(
            form.product_id.data
        )

        order = Order(

            customer_id=customer.id,

            product_id=product.id,

            quantity=form.quantity.data,

            total_price=product.price * form.quantity.data,

            notes=form.notes.data
        )

        db.session.add(order)

        db.session.commit()

        flash(
            f'Order #{order.id} placed successfully!',
            'success'
        )

        return redirect(
            url_for('orders.orders')
        )

    return render_template(
        'order_form.html',
        form=form
    )

# =========================
# CONTACT
# =========================

@orders_bp.route('/contact/', methods=['GET', 'POST'])
def contact():

    form = ContactForm()

    current_time = time.time()
    global submission_times

    # clean old submissions
    submission_times = [
        t for t in submission_times
        if current_time - t < 60
    ]

    # rate limit check
    if len(submission_times) >= 3:
        flash('Too many submissions. Please wait a minute.', 'danger')
        return redirect(url_for('orders.contact'))

    # form submit
    if form.validate_on_submit():

        submission_times.append(current_time)

        # SAVE TO DATABASE (IMPORTANT)
        from app.models import ContactMessage

        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            phone=form.phone.data,
            message=form.message.data
        )

        db.session.add(msg)
        db.session.commit()

        return render_template(
            'thank_you.html',
            name=form.name.data,
            subject=form.subject.data
        )

    # ALWAYS RETURN THIS (VERY IMPORTANT)
    return render_template(
        'contact.html',
        form=form
    )
# =========================
# STATUS API
# =========================

@orders_bp.route('/status')
def status():

    total_products = Product.query.count()

    total_orders = Order.query.count()

    return jsonify({

        'products': total_products,

        'orders': total_orders
    })