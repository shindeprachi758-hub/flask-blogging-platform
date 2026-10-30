from tests.base import BaseTestCase
from app.models import User, Post, Category, Tag
from app.extensions import db


class TestPostCRUD(BaseTestCase):
    """Test suite for Blog Post CRUD functionality and authorization."""

    def setUp(self):
        super().setUp()
        # Seed an author and category
        self.author = self.register_user(username='author1', email='author1@example.com')
        self.other_user = self.register_user(username='intruder', email='intruder@example.com')

        self.category = Category(name='Engineering', description='Software design patterns')
        db.session.add(self.category)
        db.session.commit()

    def test_create_post(self):
        """Verify creating a blog post with category and tags."""
        self.login_client(email='author1@example.com')
        response = self.client.post('/posts/create', data={
            'title': 'Understanding Python Decorators',
            'summary': 'A practical guide to Python decorators.',
            'category_id': self.category.id,
            'tags': 'python, backend, advanced',
            'content': '<p>Decorators dynamically alter the functionality of a function.</p>'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Understanding Python Decorators', response.data)

        post = Post.query.filter_by(title='Understanding Python Decorators').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author.username, 'author1')
        self.assertEqual(post.category.name, 'Engineering')
        self.assertEqual(len(post.tags), 3)
        tag_names = [t.name for t in post.tags]
        self.assertIn('python', tag_names)
        self.assertIn('backend', tag_names)

    def test_read_post_detail_and_view_increment(self):
        """Verify reading a post and view counter incrementation."""
        post = Post(
            title='Flask Architecture Deep Dive',
            content='<p>Detailed architecture breakdown.</p>',
            author=self.author,
            category=self.category,
            views=5
        )
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask Architecture Deep Dive', response.data)

        # Re-query to verify view count increased by 1
        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.views, 6)

    def test_update_post_by_owner(self):
        """Verify author can update their own post."""
        post = Post(
            title='Initial Draft Title',
            content='<p>Draft content.</p>',
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        self.login_client(email='author1@example.com')
        response = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Final Polished Title',
            'summary': 'Updated summary description.',
            'category_id': self.category.id,
            'tags': 'flask, release',
            'content': '<p>Polished and finalized content.</p>'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, 'Final Polished Title')

    def test_update_post_forbidden_for_non_owner(self):
        """Verify another user cannot edit someone else's post (403 Forbidden)."""
        post = Post(
            title='Author1 Private Post',
            content='<p>Protected content.</p>',
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        # Log in as other_user
        self.login_client(email='intruder@example.com')
        response = self.client.post(f'/posts/{post.id}/edit', data={
            'title': 'Hacked Title',
            'category_id': self.category.id,
            'content': '<p>Malicious replacement.</p>'
        })

        self.assertEqual(response.status_code, 403)
        unchanged_post = db.session.get(Post, post.id)
        self.assertEqual(unchanged_post.title, 'Author1 Private Post')

    def test_delete_post_by_owner(self):
        """Verify author can delete their own post."""
        post = Post(
            title='Post To Delete',
            content='<p>To be removed.</p>',
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        self.login_client(email='author1@example.com')
        response = self.client.post(f'/posts/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, post.id))

    def test_delete_post_forbidden_for_non_owner(self):
        """Verify another user cannot delete someone else's post (403 Forbidden)."""
        post = Post(
            title='Author1 Safe Post',
            content='<p>Content.</p>',
            author=self.author,
            category=self.category
        )
        db.session.add(post)
        db.session.commit()

        self.login_client(email='intruder@example.com')
        response = self.client.post(f'/posts/{post.id}/delete')
        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(db.session.get(Post, post.id))

    def test_create_category(self):
        """Verify category creation and uniqueness."""
        self.login_client(email='author1@example.com')
        response = self.client.post('/categories/new', data={
            'name': 'Cloud Computing',
            'description': 'AWS, Azure, and Google Cloud articles'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        cat = Category.query.filter_by(name='Cloud Computing').first()
        self.assertIsNotNone(cat)
        self.assertEqual(cat.description, 'AWS, Azure, and Google Cloud articles')
