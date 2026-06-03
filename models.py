from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt


# =========================
# USER MODEL
# =========================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default='customer')
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)


# =========================
# PRODUCT
# =========================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

    orders = db.relationship('Order', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"


# =========================
# CUSTOMER
# =========================
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"


# =========================
# ORDER
# =========================
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.Column(db.Text, default='')

    def __repr__(self):
        return f"<Order {self.id}>"
    
# =================
#  Message 
# =================

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.email}>"
# ============
# Item-Cart
# ============

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

    def subtotal(self):
        return self.quantity * self.product.price

    def __repr__(self):
        return f"<CartItem user={self.user_id} product={self.product_id}>"
    
# ===============
# Order-Item
# ===============

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)  # snapshot

    order = db.relationship('Order', backref='items')
    product = db.relationship('Product', backref='order_items')