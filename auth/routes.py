from itsdangerous import URLSafeTimedSerializer
from flask import request
from app.forms import (
    RegistrationForm,
    LoginForm,
    ResetRequestForm,
    ResetPasswordForm
)
from app.models import User
from app import db, bcrypt



from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db

from app.models import User

from app.forms import (
    RegistrationForm,
    LoginForm
)

# =========================
# BLUEPRINT
# =========================

auth_bp = Blueprint(
    'auth',
    __name__
)

serializer = URLSafeTimedSerializer('dev-secret-key')

# =========================
# REGISTER
# =========================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(url_for('orders.home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(
            name=form.name.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        db.session.add(user)

        db.session.commit()

        flash(
            'Account created successfully!',
            'success'
        )

        return redirect(url_for('auth.login'))

    return render_template(
        'register.html',
        form=form
    )

# =========================
# LOGIN
# =========================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        return redirect(url_for('orders.home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and user.check_password(
            form.password.data
        ):

            login_user(
                user,
                remember=form.remember.data
            )

            next_page = request.args.get('next')

            return redirect(
                next_page or url_for('orders.home')
            )

        flash(
            'Invalid email or password.',
            'danger'
        )

    return render_template(
        'login.html',
        form=form
    )


@auth_bp.route('/reset-request', methods=['GET', 'POST'])
def reset_request():

    form = ResetRequestForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            token = serializer.dumps(
                user.email,
                salt='password-reset'
            )

            reset_link = url_for(
                'auth.reset_password',
                token=token,
                _external=True
            )

            flash(
                f'Reset Link: {reset_link}',
                'info'
            )

            return redirect(
                url_for('auth.login')
            )

        flash(
            'Email not found.',
            'danger'
        )

    return render_template(
        'reset_request.html',
        form=form
    )

@auth_bp.route(
    '/reset-password/<token>',
    methods=['GET', 'POST']
)
def reset_password(token):

    try:

        email = serializer.loads(
            token,
            salt='password-reset',
            max_age=600
        )

    except:

        flash(
            'Invalid or expired token.',
            'danger'
        )

        return redirect(
            url_for('auth.login')
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        flash(
            'User not found.',
            'danger'
        )

        return redirect(
            url_for('auth.login')
        )

    form = ResetPasswordForm()

    if form.validate_on_submit():

        user.set_password(
            form.password.data
        )

        db.session.commit()

        flash(
            'Password updated successfully!',
            'success'
        )

        return redirect(
            url_for('auth.login')
        )

    return render_template(
        'reset_password.html',
        form=form
    )

# =========================
# LOGOUT
# =========================

@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()

    flash(
        'Logged out successfully.',
        'info'
    )

    return redirect(url_for('orders.home'))