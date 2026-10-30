from tests.base import BaseTestCase
from app.models import User, Post, Category, Comment
from app.extensions import db


class TestCommentingSystem(BaseTestCase):
    """Test suite for Blog Commenting, Authorization, and Moderation."""

    def setUp(self):
        super().setUp()
        self.post_author = self.register_user(username='writer', email='writer@example.com')
        self.commenter = self.register_user(username='commenter', email='commenter@example.com')
        self.bystander = self.register_user(username='bystander', email='bystander@example.com')

        self.category = Category(name='DevTips', description='Development tips')
        db.session.add(self.category)

        self.post = Post(
            title='Clean Code in Python',
            content='<p>Writing maintainable code is key.</p>',
            author=self.post_author,
            category=self.category
        )
        db.session.add(self.post)
        db.session.commit()

    def test_add_comment_authenticated(self):
        """Verify logged-in user can add a comment."""
        self.login_client(email='commenter@example.com')
        response = self.client.post(f'/posts/{self.post.id}/comment', data={
            'content': 'Outstanding explanation! Really appreciated the examples.'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your comment has been posted', response.data)

        comment = Comment.query.filter_by(post_id=self.post.id).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.author.username, 'commenter')
        self.assertEqual(comment.content, 'Outstanding explanation! Really appreciated the examples.')

    def test_add_comment_unauthenticated(self):
        """Verify unauthenticated user cannot post comment."""
        response = self.client.post(f'/posts/{self.post.id}/comment', data={
            'content': 'Anonymous attempt.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])
        self.assertEqual(Comment.query.count(), 0)

    def test_comment_author_can_delete_own_comment(self):
        """Verify author of a comment can delete it."""
        comment = Comment(
            content='My temporary comment.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        self.login_client(email='commenter@example.com')
        response = self.client.post(f'/comments/{comment.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Comment, comment.id))

    def test_post_author_can_moderate_comments(self):
        """Verify post owner can delete any comment on their post."""
        comment = Comment(
            content='Spammy comment from someone else.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        # Log in as the post author
        self.login_client(email='writer@example.com')
        response = self.client.post(f'/comments/{comment.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Comment, comment.id))

    def test_unauthorized_user_cannot_delete_comment(self):
        """Verify bystander cannot delete another user's comment (403 Forbidden)."""
        comment = Comment(
            content='Valuable comment.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        # Log in as bystander
        self.login_client(email='bystander@example.com')
        response = self.client.post(f'/comments/{comment.id}/delete')
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(db.session.get(Comment, comment.id))

    def test_cascade_deletion_of_comments(self):
        """Verify deleting a post automatically removes all its comments."""
        c1 = Comment(content='First comment', author=self.commenter, post=self.post)
        c2 = Comment(content='Second comment', author=self.bystander, post=self.post)
        db.session.add_all([c1, c2])
        db.session.commit()

        self.assertEqual(Comment.query.count(), 2)

        # Delete post
        db.session.delete(self.post)
        db.session.commit()

        # Comments must be removed
        self.assertEqual(Comment.query.count(), 0)
