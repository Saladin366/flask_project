from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from project import db
from ..auth.models import User
from .forms import PostForm
from .models import Favorite, Post

POST_DELETED = 'Запись удалена'
FAVORITE_EXISTS = 'Запись уже в избранном'
FAVORITE_NOT_EXISTS = 'Запись отсутствует в избранном'

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post_detail', id=post.id))
    return render_template('blog/create_post.html', form=form)


@bp.route('/posts/<int:id>/edit', methods=('GET', 'POST'),
          strict_slashes=False)
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return redirect(url_for('.post_detail', id=id))
    form = PostForm(text=post.text)
    if form.validate_on_submit():
        post.text = form.text.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post_detail', id=id))
    return render_template('blog/create_post.html', form=form)


@bp.route('/posts/<int:id>/delete', strict_slashes=False)
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return redirect(url_for('.post_detail', id=id))
    db.session.delete(post)
    db.session.commit()
    flash(POST_DELETED)
    return redirect(url_for('.index'))


@bp.route('/posts/<int:id>', strict_slashes=False)
def post_detail(id):
    post = Post.query.get_or_404(id)
    favorite = current_user.is_authenticated and Favorite.query.filter_by(
        post=post, user=current_user).first() is not None
    count = Favorite.query.filter_by(post=post).count()
    return render_template(
        'blog/post_detail.html', post=post, favorite=favorite, count=count)


@bp.route('/profile/<string:username>', strict_slashes=False)
def profile(username):
    author = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=author).order_by(Post.id.desc()).all()
    return render_template('blog/profile.html', author=author, posts=posts)


@bp.route('/posts/<int:id>/like', strict_slashes=False)
@login_required
def add_favorite(id):
    post = Post.query.get_or_404(id)
    if Favorite.query.filter_by(post=post, user=current_user).first():
        flash(FAVORITE_EXISTS)
        return redirect(url_for('.post_detail', id=id))
    favorite = Favorite(post=post, user=current_user)
    db.session.add(favorite)
    db.session.commit()
    return redirect(url_for('.post_detail', id=id))


@bp.route('/posts/<int:id>/dislike', strict_slashes=False)
@login_required
def delete_favorite(id):
    post = Post.query.get_or_404(id)
    favorite = Favorite.query.filter_by(post=post, user=current_user).first()
    if favorite is None:
        flash(FAVORITE_NOT_EXISTS)
        return redirect(url_for('.post_detail', id=id))
    db.session.delete(favorite)
    db.session.commit()
    return redirect(url_for('.post_detail', id=id))


@bp.route('/favorites', strict_slashes=False)
@login_required
def favorites():
    posts = Post.query.filter(Post.favorites.any(
        Favorite.user == current_user)).order_by(Post.id.desc()).all()
    return render_template('blog/favorites.html', posts=posts)
