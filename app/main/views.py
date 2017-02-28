from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.models import User
from . import main
from .forms import EditProfileForm


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('/main/user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updata.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('/main/edit_profile.html', form=form)
