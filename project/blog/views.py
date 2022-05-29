from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from project import db
from ..auth.models import User
from .forms import PostForm
from .models import Post

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = Post.query.order_by(-Post.id).all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'), strict_slashes=False)
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('blog/create_post.html', form=form)


@bp.route('/posts/<int:id>', strict_slashes=False)
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('blog/post_detail.html', posts=[post])


@bp.route('/profile/<string:username>', strict_slashes=False)
def profile(username):
    author = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=author).order_by(-Post.id).all()
    return render_template('blog/profile.html', author=author, posts=posts)
