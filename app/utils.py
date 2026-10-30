import bleach
import math
import hashlib
import re

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol',
    'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
    'pre', 'span', 'u', 's', 'sub', 'sup', 'img', 'table', 'thead', 'tbody',
    'tr', 'th', 'td'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'class'],
    '*': ['class']
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def sanitize_html(html_content: str) -> str:
    """Sanitize raw HTML input from rich text editors to prevent XSS attacks."""
    if not html_content:
        return ""
    cleaned = bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    return bleach.linkify(cleaned)


def calculate_reading_time(text: str) -> int:
    """Estimate reading time in minutes assuming average speed of 200 wpm."""
    if not text:
        return 1
    # Strip HTML tags for clean word count
    clean_text = re.sub(r'<[^>]+>', ' ', text)
    words = clean_text.split()
    word_count = len(words)
    minutes = math.ceil(word_count / 200)
    return max(1, minutes)


def get_gravatar_url(email: str, size: int = 80) -> str:
    """Generate Gravatar or fallback to UI-Avatars based on email."""
    if not email:
        return f"https://ui-avatars.com/api/?name=User&size={size}&background=0D6EFD&color=fff"
    encoded_email = email.strip().lower().encode('utf-8')
    digest = hashlib.md5(encoded_email).hexdigest()
    # If Gravatar doesn't exist, d=identicon or 404
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
