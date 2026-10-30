from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.extensions import db
from app.models import Post, Category, Tag, Comment
from app.forms import PostForm, CategoryForm, CommentForm
from app.utils import sanitize_html

posts_bp = Blueprint('posts', __name__)


def sync_post_tags(post, tags_string):
    """Parse comma-separated tag names and associate with the post."""
    post.tags.clear()
    if tags_string:
        raw_tags = [t.strip().lower() for t in tags_string.split(',') if t.strip()]
        # Remove duplicates while preserving order
        unique_tags = list(dict.fromkeys(raw_tags))
        for tag_name in unique_tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            post.tags.append(tag)


@posts_bp.route('/posts')
def all_posts():
    """Browse all blog posts with search, category/tag filtering, sorting, and pagination."""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    tag_name = request.args.get('tag', '').strip()
    sort_by = request.args.get('sort', 'newest')

    query = Post.query

    # Search filter (title or content)
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(or_(Post.title.ilike(search_term), Post.content.ilike(search_term)))

    # Category filter
    selected_category = None
    if category_id:
        selected_category = db.session.get(Category, category_id)
        if selected_category:
            query = query.filter(Post.category_id == category_id)

    # Tag filter
    selected_tag = None
    if tag_name:
        selected_tag = Tag.query.filter_by(name=tag_name).first()
        if selected_tag:
            query = query.filter(Post.tags.any(Tag.id == selected_tag.id))

    # Sorting
    if sort_by == 'oldest':
        query = query.order_by(Post.created_at.asc())
    elif sort_by == 'views':
        query = query.order_by(Post.views.desc(), Post.created_at.desc())
    else:  # default 'newest'
        query = query.order_by(Post.created_at.desc())

    # Pagination
    pagination = query.paginate(page=page, per_page=6, error_out=False)
    posts = pagination.items

    categories = Category.query.all()
    all_tags = Tag.query.all()

    return render_template(
        'posts/all_posts.html',
        posts=posts,
        pagination=pagination,
        categories=categories,
        all_tags=all_tags,
        search_query=search_query,
        selected_category=selected_category,
        selected_tag=selected_tag,
        sort_by=sort_by
    )


@posts_bp.route('/posts/<int:post_id>')
def detail(post_id):
    """View a single blog post, increment view count, and show discussion."""
    post = Post.query.get_or_404(post_id)

    # Increment view count
    post.views += 1
    db.session.commit()

    comment_form = CommentForm()
    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id
    ).limit(3).all()

    return render_template(
        'posts/detail.html',
        post=post,
        comment_form=comment_form,
        related_posts=related_posts
    )


@posts_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new blog post."""
    form = PostForm()

    # Populate categories dropdown
    categories = Category.query.order_by(Category.name).all()
    if not categories:
        # Create a default category if none exists
        default_cat = Category(name='Technology', description='Tech news and software development')
        db.session.add(default_cat)
        db.session.commit()
        categories = [default_cat]

    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            summary=form.summary.data.strip() if form.summary.data else '',
            content=sanitize_html(form.content.data),
            category_id=form.category_id.data,
            author=current_user
        )
        db.session.add(post)
        # Parse and link tags
        sync_post_tags(post, form.tags.data)

        db.session.commit()
        flash('Blog post published successfully!', 'success')
        return redirect(url_for('posts.detail', post_id=post.id))

    return render_template('posts/create.html', form=form, categories=categories)


@posts_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    """Edit an existing blog post. Only the author is permitted."""
    post = Post.query.get_or_404(post_id)

    # Authorization check
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    form = PostForm()
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.summary = form.summary.data.strip() if form.summary.data else ''
        post.content = sanitize_html(form.content.data)
        post.category_id = form.category_id.data

        sync_post_tags(post, form.tags.data)

        db.session.commit()
        flash('Your blog post has been updated successfully!', 'success')
        return redirect(url_for('posts.detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.summary.data = post.summary
        form.category_id.data = post.category_id
        form.tags.data = post.tag_string
        form.content.data = post.content

    return render_template('posts/edit.html', form=form, post=post, categories=categories)


@posts_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    """Delete a blog post. Only author is permitted."""
    post = Post.query.get_or_404(post_id)

    # Authorization check
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{title}" has been deleted.', 'info')
    return redirect(url_for('auth.dashboard'))


@posts_bp.route('/category/<int:category_id>')
def category_view(category_id):
    """Display posts belonging to a specific category."""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category.id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=6, error_out=False)

    return render_template('posts/category.html', category=category, posts=posts)


@posts_bp.route('/categories/new', methods=['GET', 'POST'])
@login_required
def new_category():
    """Create a new blog category."""
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else ''
        )
        db.session.add(cat)
        db.session.commit()
        flash(f'Category "{cat.name}" created successfully!', 'success')
        return redirect(url_for('posts.create'))

    return render_template('posts/new_category.html', form=form)


@posts_bp.route('/tag/<string:name>')
def tag_view(name):
    """Display posts labeled with a specific tag."""
    tag = Tag.query.filter_by(name=name.strip().lower()).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.tags.any(Tag.id == tag.id))\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=6, error_out=False)

    return render_template('posts/tag.html', tag=tag, posts=posts)
