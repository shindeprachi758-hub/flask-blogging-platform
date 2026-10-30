from tests.base import BaseTestCase
from app.models import User
from app.extensions import db


class TestAuthentication(BaseTestCase):
    """Test suite for User Authentication and Profile Management."""

    def test_user_password_hashing(self):
        """Verify Werkzeug salted password hashing."""
        u = User(username='hashuser', email='hash@example.com')
        u.set_password('SecretPass123!')
        self.assertNotEqual(u.password_hash, 'SecretPass123!')
        self.assertTrue(u.check_password('SecretPass123!'))
        self.assertFalse(u.check_password('WrongPass!'))

    def test_registration_success(self):
        """Verify new user registration flow."""
        response = self.client.post('/register', data={
            'username': 'newdeveloper',
            'email': 'developer@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successfully created', response.data)
        user = User.query.filter_by(username='newdeveloper').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'developer@example.com')

    def test_registration_duplicate_username(self):
        """Verify registration rejects existing username."""
        self.register_user(username='existinguser', email='first@example.com')
        response = self.client.post('/register', data={
            'username': 'existinguser',
            'email': 'second@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)

        self.assertIn(b'already taken', response.data)
        self.assertEqual(User.query.filter_by(username='existinguser').count(), 1)

    def test_registration_duplicate_email(self):
        """Verify registration rejects existing email address."""
        self.register_user(username='userone', email='duplicate@example.com')
        response = self.client.post('/register', data={
            'username': 'usertwo',
            'email': 'duplicate@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)

        self.assertIn(b'already exists', response.data)
        self.assertEqual(User.query.filter_by(email='duplicate@example.com').count(), 1)

    def test_login_success(self):
        """Verify successful user authentication and session creation."""
        self.register_user(username='logintest', email='login@example.com', password='Password123!')
        response = self.login_client(email='login@example.com', password='Password123!')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, logintest', response.data)

    def test_login_invalid_credentials(self):
        """Verify rejection of incorrect password."""
        self.register_user(username='wrongpassuser', email='wrong@example.com', password='Password123!')
        response = self.login_client(email='wrong@example.com', password='IncorrectPassword')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

    def test_logout(self):
        """Verify user logout session clearance."""
        self.register_user()
        self.login_client()
        response = self.logout_client()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged out successfully', response.data)

    def test_protected_routes_require_login(self):
        """Verify unauthenticated access to protected routes redirects to login."""
        protected_urls = ['/posts/create', '/dashboard', '/profile', '/categories/new']
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login', response.headers['Location'])

    def test_user_dashboard_access(self):
        """Verify authenticated user can view dashboard."""
        self.register_user()
        self.login_client()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Author Dashboard', response.data)

    def test_profile_update(self):
        """Verify user can update bio and username."""
        self.register_user(username='oldname', email='profile@example.com')
        self.login_client(email='profile@example.com')

        response = self.client.post('/profile', data={
            'username': 'newname',
            'email': 'profile@example.com',
            'bio': 'Passionate Python developer building web apps.'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'profile has been updated', response.data)
        user = User.query.filter_by(email='profile@example.com').first()
        self.assertEqual(user.username, 'newname')
        self.assertEqual(user.bio, 'Passionate Python developer building web apps.')

