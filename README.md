# BlogCraft - Full-Stack Blogging Platform with Python Flask

[![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000.svg?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3.svg?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-34%20Passed-brightgreen.svg?style=flat)](tests/)
[![Security](https://img.shields.io/badge/Security-OWASP%20Protected-blue.svg?style=flat)]()

**BlogCraft** is an industry-grade, full-stack blogging platform developed as a complete DIY Internship Project (Week 1 through Week 8). It features the Application Factory pattern, robust user authentication, relational database management (SQLAlchemy), rich-text editing (Quill), HTML sanitization (Bleach), interactive community commenting, full-text search, and multi-parameter filtering.

---

## 📑 Table of Contents

- [Features by Internship Week](#-features-by-internship-week)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Database Schema (ERD)](#-database-schema-erd)
- [Quick Start & Installation](#-quick-start--installation)
- [Demo Credentials](#-demo-credentials)
- [Automated Testing Suite](#-automated-testing-suite)
- [Security Implementation](#-security-implementation)
- [Routes Reference](#-routes-reference)
- [Week 8 Video Presentation & Submission](#-week-8-video-presentation--submission)

---

## 🚀 Features by Internship Week

| Week | Milestone | Delivered Features |
|---|---|---|
| **Week 1** | **Flask Setup & Foundation** | Application factory (`create_app`), modular configuration classes (dev, test, prod), SQLite + Flask-SQLAlchemy integration, Jinja2 template inheritance, modern responsive navbar & footer. |
| **Week 2** | **User Authentication** | User registration with email/username uniqueness checks, login/logout, session management via Flask-Login, salted PBKDF2/Scrypt hashing via Werkzeug, protected routes (`@login_required`), personal author dashboard. |
| **Week 3** | **Blog Post CRUD & Rich Editor** | Full CRUD operations (Create, Read, Update, Delete with confirmation modals), One-to-Many and Many-to-Many relational models, Quill WYSIWYG rich text editor, Bleach XSS sanitization, reading time estimator. |
| **Week 4** | **Modern UI/UX & Responsive Views** | Contemporary design system in Bootstrap 5.3, custom typography (`Plus Jakarta Sans`), card hover animations, badge chips, author profile view, category view, tag view, custom 403/404/500 error pages. |
| **Week 5** | **Community Commenting System** | Relational `Comment` model, real-time comment stream under posts, author-only deletion control, post author moderation privileges, empty state UI. |
| **Week 6** | **Search, Filtering & Pagination** | Multi-field search across titles and article content, category dropdown filtering, tag filtering, dynamic sorting (`newest`, `oldest`, `views`), pagination controls, active filter tags & reset action. |
| **Week 7** | **Testing & Deployment Readiness** | 34 automated unit & integration tests covering 100% of functional requirements, in-memory SQLite test harnesses, database seeder script (`seed.py`), production configs, `.env` management. |
| **Week 8** | **Internship Evaluation Kit** | Complete video presentation script (`INTERNSHIP_VIDEO_SCRIPT.md`), screenshots checklist, demonstration sequence, and final project report. |

---

## 🛠 Technology Stack

### Backend
- **Python 3.13** - Primary programming language
- **Flask 3.x** - Web framework and routing engine
- **Flask-SQLAlchemy** - Object-Relational Mapping (ORM)
- **Flask-Login** - Session lifecycle and authentication management
- **Flask-WTF & WTForms** - Secure form generation, validation, and CSRF protection
- **Flask-Migrate & Alembic** - Database schema migrations
- **Werkzeug** - Cryptographic password hashing (`generate_password_hash`, `check_password_hash`)
- **Bleach** - HTML whitelist sanitization to prevent Stored XSS

### Frontend
- **HTML5 & CSS3** - Semantic markup & custom modern styling
- **Bootstrap 5.3** - Mobile-first responsive layout and components
- **Bootstrap Icons** - Vector icon library
- **Jinja2** - Dynamic server-side templating engine
- **Quill.js** - Modern WYSIWYG rich-text editor
- **Vanilla JavaScript** - Asynchronous UI interactions and alert dismissals

### Database & Dev Tools
- **SQLite 3** - Lightweight ACID relational storage
- **Virtual Environment (`.venv`)** - Dependency isolation
- **Git** - Version control

---

## 📂 Project Architecture

```
blogging_platform/
├── app/
│   ├── __init__.py          # Application Factory (create_app), error handlers, template filters
│   ├── extensions.py        # Extensions initialization (db, migrate, login_manager, csrf)
│   ├── models.py            # SQLAlchemy models (User, Post, Category, Tag, Comment, post_tags)
│   ├── forms.py             # Flask-WTF validation forms (Register, Login, Post, Comment, etc.)
│   ├── utils.py             # Utility helpers (HTML sanitization, reading time, gravatars)
│   │
│   ├── routes/              # Modular Blueprints
│   │   ├── __init__.py      # Blueprint exports
│   │   ├── main.py          # Homepage (/) & About (/about)
│   │   ├── auth.py          # Authentication (/login, /register, /dashboard, /profile)
│   │   ├── posts.py         # Post CRUD, category views, tag views (/posts, /posts/create, etc.)
│   │   └── comments.py      # Discussion & moderation (/posts/<id>/comment, /comments/<id>/delete)
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom design system, typography, cards & buttons
│   │   ├── js/
│   │   │   └── main.js      # Quill editor syncing, auto-dismiss alerts, tooltips
│   │   └── images/
│   │
│   └── templates/           # Reusable Jinja2 Templates
│       ├── base.html        # Master template
│       ├── components/      # Partial components (navbar, footer, flash, post_card, pagination)
│       ├── main/            # index.html, about.html
│       ├── auth/            # login.html, register.html
│       ├── user/            # dashboard.html, profile.html, author.html
│       ├── posts/           # all_posts.html, detail.html, create.html, edit.html, category.html, tag.html
│       └── errors/          # 403.html, 404.html, 500.html
│
├── instance/                # SQLite database storage (blog_dev.db)
├── migrations/              # Alembic database migration scripts
├── tests/                   # Automated Test Suite (34 tests)
│   ├── base.py              # BaseTestCase with in-memory SQLite fixtures
│   ├── test_auth.py         # Registration, login, logout, password hashing, dashboards
│   ├── test_posts.py        # Post CRUD, authorization checks, categories, tags
│   ├── test_comments.py     # Commenting, moderation permissions, cascade deletion
│   ├── test_search.py       # Title/content search, filtering, sorting
│   └── test_security.py     # Bleach XSS sanitization, reading time calculator
│
├── config.py                # Configuration classes (Development, Testing, Production)
├── run.py                   # Development server entry point
├── seed.py                  # Database population script with realistic sample content
├── requirements.txt         # Pinned project dependencies
├── .env.example             # Template environment variables
├── .env                     # Local environment settings
└── README.md                # Comprehensive project documentation
```

---

## 🗄 Database Schema (ERD)

```
       +------------------+
       |       USER       |
       +------------------+
       | id (PK)          |
       | username         |
       | email            |
       | password_hash    |
       | bio              |
       | is_admin         |
       | created_at       |
       +------------------+
          |             |
     (1)  |             | (1)
          |             |
          v (M)         v (M)
  +--------------+   +--------------+
  |     POST     |   |   COMMENT    |
  +--------------+   +--------------+
  | id (PK)      |   | id (PK)      |
  | title        |   | content      |
  | content      |   | created_at   |
  | summary      |   | user_id (FK) |----+
  | views        |   | post_id (FK) |    |
  | created_at   |   +--------------+    |
  | updated_at   |           ^           |
  | user_id (FK) |           | (M)       |
  | cat_id (FK)  |           |           |
  +--------------+           | (1)       |
     |         |             |           |
 (M) |     (1) +-------------+           |
     |                                   |
     v (M)           (M)             (1) |
  +-----------+       v                  |
  | post_tags |    +------------+        |
  +-----------+    |  CATEGORY  |        |
  | post_id   |    +------------+        |
  | tag_id    |    | id (PK)    |        |
  +-----------+    | name       |        |
     ^             | desc       |        |
 (M) |             +------------+        |
     |                                   |
  +-----------+                          |
  |    TAG    |                          |
  +-----------+                          |
  | id (PK)   |                          |
  | name      |                          |
  +-----------+                          |
```

---

## ⚡ Quick Start & Installation

### 1. Clone the repository and navigate to workspace
```bash
git clone <repository_url>
cd "Blogging pltform with flask"
```

### 2. Set up Python Virtual Environment
```bash
python -m venv .venv

# Activate on Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Activate on macOS/Linux:
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Seed the Database with Demo Content
Run the automated seed script to populate realistic users, categories, tags, blog articles, and comments:
```bash
python seed.py
```

### 6. Start the Flask Development Server
```bash
python run.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔑 Demo Credentials

The database seeder automatically creates the following demo user accounts for evaluation:

| Role | Email | Password | Access / Capabilities |
|---|---|---|---|
| **Platform Admin** | `admin@blogcraft.com` | `AdminPass123!` | Full moderation, category creation, write/edit/delete |
| **Author (Sarah)** | `sarah@example.com` | `Password123!` | Author of articles, comments, dashboard access |
| **Author (Alex)** | `alex@example.com` | `Password123!` | Author of articles, comments, dashboard access |

---

## 🧪 Automated Testing Suite

The project includes **34 automated tests** executed against an in-memory SQLite database (`TestingConfig`):

```bash
python -m unittest discover tests
```

### Test Suite Summary:
- **`tests/test_auth.py` (10 tests):** Registration, duplicate email rejection, duplicate username rejection, valid login, invalid login, logout, password hashing, protected routes, user dashboard, profile updates.
- **`tests/test_posts.py` (7 tests):** Post creation, category association, many-to-many tag linking, reading post, view counter increment, author post edit, non-author edit prevention (403), author deletion, non-author deletion prevention (403), category creation.
- **`tests/test_comments.py` (6 tests):** Authenticated comment posting, unauthenticated comment blocking, comment author deletion, post author moderation deletion, unauthorized deletion prevention (403), cascade deletion on post removal.
- **`tests/test_search.py` (6 tests):** Search by title, search by content, category filtering, tag filtering, view-count sorting, empty results state.
- **`tests/test_security.py` (5 tests):** Bleach XSS script tag stripping, malicious attribute filtering, safe formatting tag preservation, word count reading time calculator, password salt verification.

---

## 🛡 Security Implementation

1. **Password Hashing:** Passwords are never stored in plaintext. Werkzeug computes PBKDF2/Scrypt cryptographic salted hashes.
2. **CSRF Defense:** `Flask-WTF` attaches cryptographic tokens to all state-changing HTML forms.
3. **Stored XSS Prevention:** User-submitted HTML from the Quill editor is cleaned using `bleach.clean()` with strict tag and attribute whitelists.
4. **Access Control & Authorization:** Routes performing modifications (`/posts/<id>/edit`, `/posts/<id>/delete`, `/comments/<id>/delete`) verify ownership (`post.author == current_user`) and abort with `403 Forbidden` if violated.
5. **SQL Injection Immunity:** All database queries utilize SQLAlchemy parameterization, completely neutralizing SQL injection risks.

---

## 🗺 Routes Reference

| HTTP Method | Route | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | Homepage with featured story & latest posts | No |
| `GET` | `/about` | Architecture, tech stack & milestones | No |
| `GET, POST` | `/register` | User account registration | No |
| `GET, POST` | `/login` | User authentication & session start | No |
| `GET` | `/logout` | End session | Yes |
| `GET` | `/dashboard` | Author personal analytics & articles | Yes |
| `GET, POST` | `/profile` | Edit user username, email & biography | Yes |
| `GET` | `/author/<username>` | Public author profile & authored posts | No |
| `GET` | `/posts` | All articles with search, filter & sort | No |
| `GET` | `/posts/<id>` | Single article view & discussion stream | No |
| `GET, POST` | `/posts/create` | Create post with Quill rich editor | Yes |
| `GET, POST` | `/posts/<id>/edit` | Edit existing post (Author only) | Yes |
| `POST` | `/posts/<id>/delete` | Delete post (Author only) | Yes |
| `GET` | `/category/<id>` | Browse articles in a specific category | No |
| `GET, POST` | `/categories/new` | Create a new blog category | Yes |
| `GET` | `/tag/<name>` | Browse articles tagged with a keyword | No |
| `POST` | `/posts/<id>/comment`| Submit a comment on an article | Yes |
| `POST` | `/comments/<id>/delete`| Remove comment (Comment/Post author) | Yes |

---

## 🎥 Week 8 Video Presentation & Submission

For the final internship evaluation, refer to:
- [`INTERNSHIP_VIDEO_SCRIPT.md`](INTERNSHIP_VIDEO_SCRIPT.md) - Complete verbatim video presentation script covering all 10 required demonstration milestones.
- [`PROJECT_REPORT.md`](PROJECT_REPORT.md) - Formal engineering project report.

