from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import SignupForm, LoginForm, UpdateAccountForm, RequestPasswordResetForm, ResetPasswordForm
from flaskblog.users.utils import save_thumbnail, send_password_reset_email

users = Blueprint('users', __name__)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been successfully created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', title='Sign up', legend='Sign up', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login failed! Please check your username and password!', 'danger')
    return render_template('login.html', title='Log in', legend='Log in', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.new_thumbnail.data:
            new_thumbnail = save_thumbnail(form.new_thumbnail.data)
            current_user.thumbnail = new_thumbnail
        current_user.username = form.new_username.data
        current_user.email = form.new_email.data
        db.session.commit()
        flash('Your account has been successfully updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.new_username.data = current_user.username
        form.new_email.data = current_user.email
    thumbnail = url_for('static', filename='thumbnails/' + current_user.thumbnail)
    return render_template('profile.html', title=f"{current_user.username}'s profile", legend='Update profile', thumbnail=thumbnail, form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash('An email with instructions on how to reset your password has been sent to your mailbox.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset password', legend='Reset password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been successfully updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset password', legend='Reset password', form=form)
