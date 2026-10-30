from tests.base import BaseTestCase
from app.models import User, Post, Category, Tag
from app.extensions import db


class TestSearchAndFiltering(BaseTestCase):
    """Test suite for search, filtering, and sorting functionality."""

    def setUp(self):
        super().setUp()
        self.user = self.register_user()

        self.cat_python = Category(name='Python')
        self.cat_javascript = Category(name='JavaScript')
        db.session.add_all([self.cat_python, self.cat_javascript])

        self.tag_web = Tag(name='web')
        self.tag_backend = Tag(name='backend')
        db.session.add_all([self.tag_web, self.tag_backend])

        # Create Post A
        self.post_a = Post(
            title='FastAPI vs Flask Performance Benchmarks',
            content='Comparing ASGI and WSGI execution metrics and memory footprints.',
            author=self.user,
            category=self.cat_python,
            views=100
        )
        self.post_a.tags.append(self.tag_backend)

        # Create Post B
        self.post_b = Post(
            title='React and Vue Frontend Comparison',
            content='State management and component lifecycle in modern frontend frameworks.',
            author=self.user,
            category=self.cat_javascript,
            views=250
        )
        self.post_b.tags.append(self.tag_web)

        db.session.add_all([self.post_a, self.post_b])
        db.session.commit()

    def test_search_by_title(self):
        """Verify keyword search matching post title."""
        response = self.client.get('/posts?q=FastAPI')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FastAPI vs Flask', response.data)
        self.assertNotIn(b'React and Vue', response.data)

    def test_search_by_content(self):
        """Verify keyword search matching post content."""
        response = self.client.get('/posts?q=lifecycle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'React and Vue', response.data)
        self.assertNotIn(b'FastAPI vs Flask', response.data)

    def test_filter_by_category(self):
        """Verify filtering posts by category ID."""
        response = self.client.get(f'/posts?category={self.cat_python.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FastAPI vs Flask', response.data)
        self.assertNotIn(b'React and Vue', response.data)

    def test_filter_by_tag(self):
        """Verify filtering posts by tag name."""
        response = self.client.get('/posts?tag=backend')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FastAPI vs Flask', response.data)
        self.assertNotIn(b'React and Vue', response.data)

    def test_sorting_by_views(self):
        """Verify sorting posts by view count in descending order."""
        response = self.client.get('/posts?sort=views')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        pos_b = data.find('React and Vue')
        pos_a = data.find('FastAPI vs Flask')
        self.assertTrue(pos_b < pos_a)

    def test_no_results_found_message(self):
        """Verify helpful empty state message when search returns zero results."""
        response = self.client.get('/posts?q=NonExistentKeywordXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Matching Articles Found', response.data)

