# DIY INTERNSHIP FINAL PROJECT REPORT
# TITLE: BLOGGING PLATFORM WITH PYTHON FLASK (BLOGCRAFT)

**Project Track:** Full-Stack Web Development Internship  
**Frameworks & Libraries:** Python 3.13, Flask 3.x, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Bootstrap 5.3, SQLite 3, Bleach, Quill.js  
**Submission Date:** October 2026  
**Status:** 100% Completed & Verified  

---

## 1. EXECUTIVE SUMMARY

The **BlogCraft Blogging Platform** is a full-stack, secure, modular web application engineered across an intensive 8-week software development lifecycle. The project demonstrates the complete process of building an enterprise-grade content management system—from architectural planning and relational data modeling to user authentication, rich-text authoring, community engagement, search algorithms, automated testing, and deployment preparation.

The final platform provides an intuitive, high-performance experience for both article writers and community readers while rigorously adhering to modern web security standards (OWASP Top 10 mitigation, Werkzeug password hashing, CSRF tokens, and Bleach HTML sanitization).

---

## 2. WEEK-BY-WEEK MILESTONE EXECUTION

### Week 1: Flask Setup & Basic Foundation
- **Objectives:** Establish the core application architecture and environment.
- **Implementation:**
  - Adopted the Flask **Application Factory Pattern** (`create_app()`) in `app/__init__.py`.
  - Configured multi-tier configuration environments in `config.py` (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`).
  - Integrated SQLite database with `Flask-SQLAlchemy` and initialized database extensions.
  - Built Jinja2 master base layout (`base.html`), reusable navigation bar, and footer with Bootstrap 5.3 CDN.
  - Implemented responsive homepage with hero section and statistics overview.
- **Verification:** Development server started on port 5000 and served homepage with HTTP 200.

### Week 2: User Authentication System
- **Objectives:** Implement secure user identity, authentication, and session management.
- **Implementation:**
  - Designed `User` model with `username`, `email`, `password_hash`, `bio`, and `created_at`.
  - Used Werkzeug’s cryptographic routines (`generate_password_hash`, `check_password_hash`) to ensure passwords are never stored in plaintext.
  - Integrated `Flask-Login` (`LoginManager`) with `@login_manager.user_loader` callback, session cookies, and login redirection.
  - Created Flask-WTF forms for Registration (with custom username and email uniqueness validators) and Login.
  - Built protected routes guarded with `@login_required` (e.g. `/dashboard`, `/profile`, `/posts/create`).
  - Developed Author Analytics Dashboard (`/dashboard`) displaying total posts, views, and comments.
- **Verification:** Tested registration of unique accounts, session persistence, logout, and unauthorized redirect guards.

### Week 3: Blog Post CRUD Functionality & Rich Text Editor
- **Objectives:** Implement core CRUD workflows, relational database models, and WYSIWYG authoring.
- **Implementation:**
  - Created SQLAlchemy models:
    - `Post`: One-to-Many with `User`, One-to-Many with `Category`, Many-to-Many with `Tag`.
    - `Category`: One-to-Many with `Post`.
    - `Tag`: Many-to-Many with `Post` via `post_tags` junction table.
  - Implemented all 4 CRUD operations:
    - **Create:** Form supporting title, summary, category dropdown, comma-separated tags, and rich body.
    - **Read:** Single article detail view with reading time calculator and view counter.
    - **Update:** Author-exclusive edit route prefilling existing post values and updating timestamps.
    - **Delete:** Author-exclusive delete route with Bootstrap confirmation modal.
  - Integrated **Quill.js** WYSIWYG editor with customized formatting toolbar.
  - Added **Bleach** HTML sanitization in `app/utils.py` to strip unauthorized tags and attributes, preventing Cross-Site Scripting (XSS).
- **Verification:** Verified CRUD operations, Many-to-Many tag associations, and authorization barriers returning 403 Forbidden for non-authors.

### Week 4: Frontend UI/UX & Responsive Views
- **Objectives:** Design a modern, clean, responsive frontend suitable for production.
- **Implementation:**
  - Authored custom CSS design system (`app/static/css/style.css`) using the `Plus Jakarta Sans` font family.
  - Created reusable post card components (`components/post_card.html`) with category badges, author chips, view badges, and reading time.
  - Built complete page suite:
    - Homepage (`index.html`) with hero banner and featured spotlight.
    - Explore Posts (`all_posts.html`) with filter controls.
    - Single Post Detail (`detail.html`) with breadcrumb navigation.
    - Category Overview (`category.html`) and Tag Overview (`tag.html`).
    - Author Profile (`author.html`) with biography and published articles.
    - Custom error handlers (`403.html`, `404.html`, `500.html`).
- **Verification:** Tested responsive layouts across mobile (375px), tablet (768px), and desktop (1440px) viewports.

### Week 5: Commenting & Community Discussion
- **Objectives:** Implement real-time article discussions and content moderation.
- **Implementation:**
  - Created `Comment` model linked to `User` and `Post` with cascading deletion.
  - Built `CommentForm` with content length validation.
  - Displayed comments under articles with author avatar and formatted timestamps.
  - Implemented authorization logic allowing comment authors to delete their comments and post owners to moderate/delete comments on their articles.
- **Verification:** Verified comment posting, unauthenticated blocking, author deletion, and cascade removal when a parent post is deleted.

### Week 6: Search, Filtering & Sorting System
- **Objectives:** Enable efficient discovery across articles.
- **Implementation:**
  - Multi-column search utilizing SQLAlchemy `ilike` queries across both `Post.title` and `Post.content`.
  - Dynamic category filtering and tag filtering.
  - Multiple sort orders: Newest First (`created_at DESC`), Oldest First (`created_at ASC`), and Most Popular (`views DESC`).
  - Clean pagination with previous/next controls and preserved query parameters.
  - Interactive active filter chips with individual remove buttons and a "Clear All" action.
  - User-friendly empty state when zero results match the search criteria.
- **Verification:** Verified multi-parameter combinations, sorting orders, and empty state rendering.

### Week 7: Testing, Optimization & Deployment Readiness
- **Objectives:** Execute automated quality assurance and prepare for production deployment.
- **Implementation:**
  - Developed 34 automated unit and integration tests under `tests/` covering authentication, post CRUD, authorization, comments, search, and security.
  - Created automated database seeder (`seed.py`) with sample data for demonstration.
  - Configured `.env.example`, `.env`, `.gitignore`, and `requirements.txt`.
- **Verification:** All 34 automated tests passed with 100% success rate in under 9 seconds.

### Week 8: Presentation & Submission Deliverables
- **Objectives:** Prepare project documentation and evaluation walkthrough materials.
- **Implementation:**
  - Created comprehensive `README.md` with architectural diagrams, ERD schema, and route references.
  - Authored verbatim video demonstration script (`INTERNSHIP_VIDEO_SCRIPT.md`) covering all 10 required presentation milestones.
  - Prepared screenshots checklist and submission verification matrix.

---

## 3. ARCHITECTURE & DATA DESIGN

```
+-------------------------------------------------------------+
|                         PRESENTATION                        |
|   Bootstrap 5.3  *  Quill Editor  *  Jinja2 Reusable Cards  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                         APPLICATION                         |
|   Blueprints: [main_bp] [auth_bp] [posts_bp] [comments_bp]  |
|   Middlewares: Flask-Login Session, Flask-WTF CSRF Protect  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                         PERSISTENCE                         |
|        SQLAlchemy ORM (User, Post, Category, Tag, Comment)  |
|        SQLite 3 Relational Database (blog_dev.db)           |
+-------------------------------------------------------------+
```

---

## 4. AUTOMATED TEST SUITE EXECUTION REPORT

Automated test execution output from `python -m unittest discover tests`:

| Test Module | Tests Run | Pass | Fail | Tested Functionality |
|---|---|---|---|---|
| `test_auth.py` | 10 | 10 | 0 | Registration, uniqueness, login, logout, password hashing, dashboard, profile edit |
| `test_posts.py` | 7 | 7 | 0 | Post create, read, view increment, update, delete, 403 non-owner edit/delete prevention |
| `test_comments.py` | 6 | 6 | 0 | Add comment, login requirement, comment delete, post owner moderation, cascade delete |
| `test_search.py` | 6 | 6 | 0 | Title search, content search, category filter, tag filter, view count sort, empty state |
| `test_security.py` | 5 | 5 | 0 | Bleach script stripping, attribute sanitization, safe HTML retention, reading time, password salt |
| **TOTAL** | **34** | **34** | **0** | **100% Pass Rate (Duration: 8.5 seconds)** |

---

## 5. SECURITY AUDIT & DEFENSE SUMMARY

1. **Broken Access Control Mitigation (OWASP #1):**
   - Protected routes enforce authentication checks via `@login_required`.
   - Modifying or deleting posts and comments explicitly checks `resource.author == current_user` and issues `abort(403)` on mismatch.
2. **Cryptographic Failures Mitigation (OWASP #2):**
   - Passwords hashed using PBKDF2 with SHA-256 and cryptographic salts. Plaintext passwords never enter database tables.
3. **Injection Mitigation (OWASP #3):**
   - Cross-Site Scripting (XSS) thwarted by sanitizing user-submitted HTML through `bleach.clean()` before saving and rendering.
   - SQL Injection thwarted through SQLAlchemy query parameterization.
4. **Cross-Site Request Forgery (CSRF):**
   - Form submissions enforce cryptographically signed CSRF tokens generated by `Flask-WTF`.

---

## 6. CONCLUSION

The **BlogCraft Blogging Platform** satisfies all criteria of the 8-Week DIY Internship syllabus. The project demonstrates full-stack software development competency, clean coding standards, robust security practices, and thorough documentation. It is fully prepared for local execution, mentor evaluation, and cloud deployment.

