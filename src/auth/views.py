from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from src.auth import auth
from src.models import User
from src.email import send_email
from src.auth.forms import LoginForm, RegistrationForm
from src import db


# GET:  Display the login form.
# POST: Validates the email address and the password to deny or grant access.
#
# If access is denied the user is redirected to the login page to try again.
# If access is granted the user is logged in and redirected to the home page, or 
# the secure page the user was attempting to access before being prompted to login.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            # The "next" page the user was trying to access.
            next = request.args.get('next')
            # Checks that the next page is a relative URL.
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


# Logs the user out. The user must be logged in to log out.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


# GET: Display the registration form.
# POST: Validates the form and creates a new user in the database.
#
# If the form is invalid the user is redirected to the registration page to try
# again.
# If the form is valid the user is registered and redirected to the home page.
# The user must confirm their email before they can login.
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            bio=form.bio.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Account', 'auth/mail/confirm', 
            user=user, token=token)
        flash('Please confirm your email. An email has just been sent to you.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


# Sets the user's confirmed attribute to True if the token is valid. Otherwise,
# the user is redirected to the home page. 
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Your account has been confirmed!')
    else:
        flash('The link is invalid or expired.')
    return redirect(url_for('main.index'))


# Generates a new token and sends it to the user's email address.
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Account', 'auth/mail/confirm',
        user=current_user, token=token)
    flash('A new confirmation email has been sent to you.')
    return redirect(url_for('main.index'))


# Display the unconfirmed page.
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


# Before any request is made, the user is checked to see if the user is logged
# in and not confirmed, and if so, the user is redirected to the unconfirmed page.
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
        and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
