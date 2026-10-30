from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, ProfileEditForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user account."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate and log in an existing user."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')

            # Validate next URL to avoid open redirect vulnerabilities
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('auth.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out current user and clear session."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard displaying user posts, statistics, and quick actions."""
    page = request.args.get('page', 1, type=int)
    posts_pagination = Post.query.filter_by(user_id=current_user.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    # Compute author statistics
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    total_posts = len(user_posts)
    total_views = sum(post.views for post in user_posts)
    total_comments = sum(post.comments.count() for post in user_posts)

    return render_template(
        'user/dashboard.html',
        posts=posts_pagination.items,
        pagination=posts_pagination,
        total_posts=total_posts,
        total_views=total_views,
        total_comments=total_comments
    )


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and update current user's profile information."""
    form = ProfileEditForm(original_user=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.email = form.email.data.strip().lower()
        current_user.bio = form.bio.data.strip() if form.bio.data else ''
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('user/profile.html', form=form, user=current_user)


@auth_bp.route('/author/<string:username>')
def author_profile(username):
    """Public author profile page displaying bio and published articles."""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=6, error_out=False)

    return render_template('user/author.html', author=user, posts=posts)

