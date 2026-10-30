import unittest
from app import create_app
from app.extensions import db
from app.models import User, Category, Tag, Post, Comment


class BaseTestCase(unittest.TestCase):
    """Base test case initializing Flask in-memory test environment."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Create all tables in in-memory database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, username='testuser', email='test@example.com', password='Password123!'):
        """Helper to create and return a user instance."""
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def login_client(self, email='test@example.com', password='Password123!'):
        """Helper to log into the test client."""
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def logout_client(self):
        """Helper to log out from the test client."""
        return self.client.get('/logout', follow_redirects=True)

