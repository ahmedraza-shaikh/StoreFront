from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    @app.template_filter('currency')
    def currency(value):

        try:
            return f"₹{value:,.2f}"

        except:
            return f"₹{value}"

    # =========================
    # IMPORT BLUEPRINTS
    # =========================

    from app.auth.routes import auth_bp
    from app.orders.routes import orders_bp
    from app.admin.routes import admin_bp
    from app.api.routes import api_bp
    from app.cart import cart_bp
    
    # =========================
    # REGISTER BLUEPRINTS
    # =========================

    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.register_blueprint(orders_bp)

    app.register_blueprint(admin_bp, url_prefix="/admin")

    app.register_blueprint(api_bp, url_prefix="/api")

    app.register_blueprint(cart_bp, url_prefix="/cart")


    return app


from app.models import User


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))






from flask_wtf import FlaskForm
from wtforms import (
    StringField, FloatField, BooleanField,
    TextAreaField, SubmitField,
    PasswordField
)

from wtforms.validators import (
    DataRequired, Length, NumberRange, EqualTo
)

# =========================
# PRODUCT FORM
# =========================
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=1)])
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description')
    in_stock = BooleanField('In Stock')
    submit = SubmitField('Save Product')

# =========================
# REGISTER
# =========================
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

# =========================
# LOGIN
# =========================
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# =========================
# RESET PASSWORD
# =========================
class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')


