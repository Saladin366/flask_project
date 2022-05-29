from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from project import db

from .forms import LoginForm, SignUpForm
from .models import User

CHECK_EMAIL = 'Проверьте входные данные'
LOGOUT = 'Вы вышли из своей учётной записи'

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'), strict_slashes=False)
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        user = User(username=username, first_name=first_name,
                    last_name=last_name, email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/signup.html', form=form)


@bp.route('/login', methods=('GET', 'POST'), strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.email_login.data.lower()
        user = (User.query.filter_by(email=data).first() or
                User.query.filter_by(username=data).first())
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(
                request.args.get('next', None) or url_for('blog.index'))
        flash(CHECK_EMAIL)
        return redirect(url_for('.login'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(request.args.get('next', None) or url_for('.login'))
