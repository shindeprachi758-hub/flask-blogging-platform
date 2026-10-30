from flask import Blueprint, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Post, Comment
from app.forms import CommentForm
from app.utils import sanitize_html

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a blog post."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=sanitize_html(form.content.data.strip()),
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Comment error: {error}', 'danger')

    return redirect(url_for('posts.detail', post_id=post.id, _anchor='comments'))


@comments_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment. Only comment author or post author is allowed."""
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id

    # Authorization check
    if comment.author != current_user and comment.post.author != current_user and not current_user.is_admin:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been removed.', 'info')
    return redirect(url_for('posts.detail', post_id=post_id, _anchor='comments'))

