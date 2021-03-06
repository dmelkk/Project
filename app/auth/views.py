from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm
from . import auth
from ..email import send_email
from ..models import User
from .. import db


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    confirmed=True #remove when email sending will work
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        """
        temporary measures, because it's not working
        send_email(
                subject='confirm your account',
                recipients=[user.email],
                template='auth/email/confirm',
                token=token,
                user=user
                )
        """
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account, Thanks!')
    else:
        flash('Your confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
            subject='confirm your account',
            recipients=[current_user.email],
            template='auth/email/confirm',
            token=token,
            user=current_user
            )
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
