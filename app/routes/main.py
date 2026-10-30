from flask import Blueprint, render_template, request
from app.models import Post, Category, Tag

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage: shows hero section, featured post, latest posts, and popular categories."""
    featured_post = Post.query.order_by(Post.views.desc(), Post.created_at.desc()).first()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    popular_tags = Tag.query.limit(12).all()

    total_posts = Post.query.count()
    total_categories = Category.query.count()

    return render_template(
        'main/index.html',
        featured_post=featured_post,
        recent_posts=recent_posts,
        categories=categories,
        popular_tags=popular_tags,
        total_posts=total_posts,
        total_categories=total_categories
    )


@main_bp.route('/about')
def about():
    """About page outlining the Blogging Platform architecture and technology stack."""
    return render_template('main/about.html')

