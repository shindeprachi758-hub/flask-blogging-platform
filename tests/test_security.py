import unittest
from app.utils import sanitize_html, calculate_reading_time
from app.models import User


class TestSecurityAndSanitization(unittest.TestCase):
    """Test suite for XSS sanitization, password hashing, and input validation."""

    def test_xss_script_tags_stripped(self):
        """Verify dangerous <script> tags are removed by bleach."""
        malicious_input = '<p>Normal text</p><script>alert("XSS Attack!");</script>'
        cleaned = sanitize_html(malicious_input)
        self.assertNotIn('<script>', cleaned)
        self.assertNotIn('</script>', cleaned)
        self.assertIn('<p>Normal text</p>', cleaned)

    def test_xss_onerror_attribute_stripped(self):
        """Verify inline malicious JS attributes like onerror or onload are removed."""
        malicious_input = '<img src="invalid.jpg" onerror="alert(\'XSS\')" alt="Test Image">'
        cleaned = sanitize_html(malicious_input)
        self.assertNotIn('onerror', cleaned)
        self.assertIn('src="invalid.jpg"', cleaned)
        self.assertIn('alt="Test Image"', cleaned)


    def test_safe_html_formatting_preserved(self):
        """Verify permitted typography tags (headings, bold, lists, quotes) remain intact."""
        safe_input = '<h2>Header</h2><p><strong>Bold</strong> and <em>Italic</em></p><ul><li>Item 1</li></ul>'
        cleaned = sanitize_html(safe_input)
        self.assertIn('<h2>Header</h2>', cleaned)
        self.assertIn('<strong>Bold</strong>', cleaned)
        self.assertIn('<em>Italic</em>', cleaned)
        self.assertIn('<li>Item 1</li>', cleaned)

    def test_reading_time_estimation(self):
        """Verify reading time calculation based on word count."""
        short_text = "<p>Short sample text.</p>"
        self.assertEqual(calculate_reading_time(short_text), 1)

        # 450 words should be ~3 minutes
        long_text = "word " * 450
        self.assertEqual(calculate_reading_time(long_text), 3)

    def test_password_never_stored_in_plaintext(self):
        """Verify password_hash never equals the raw password."""
        raw_pw = 'SuperSecret2026!'
        u = User(username='secuser', email='sec@example.com')
        u.set_password(raw_pw)

        self.assertNotEqual(u.password_hash, raw_pw)
        self.assertTrue(u.password_hash.startswith('scrypt:') or u.password_hash.startswith('pbkdf2:'))
