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