"""
Database Seeding Script for Blogging Platform
Populates initial sample categories, tags, demo users, posts, and comments.
"""
from app import create_app
from app.extensions import db
from app.models import User, Category, Tag, Post, Comment

app = create_app('development')

def seed_database():
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding Users...")
        admin = User(
            username='admin',
            email='admin@blogcraft.com',
            bio='Lead Full-Stack Architect & Platform Administrator.',
            is_admin=True
        )
        admin.set_password('AdminPass123!')

        sarah = User(
            username='sarah_dev',
            email='sarah@example.com',
            bio='Full-stack engineer enthusiastic about Python, Flask, and elegant UI/UX design.'
        )
        sarah.set_password('Password123!')

        alex = User(
            username='alex_writer',
            email='alex@example.com',
            bio='Tech journalist and cloud computing evangelist sharing best practices.'
        )
        alex.set_password('Password123!')

        db.session.add_all([admin, sarah, alex])
        db.session.commit()

        print("Seeding Categories...")
        cat_flask = Category(
            name='Python & Flask',
            description='In-depth tutorials, tips, and architectural patterns for Flask web applications.'
        )
        cat_webdev = Category(
            name='Web Development',
            description='Frontend frameworks, modern responsive design, Bootstrap 5, and JavaScript.'
        )
        cat_ai = Category(
            name='Artificial Intelligence',
            description='Exploring machine learning, generative AI, LLMs, and real-world implementations.'
        )
        cat_devops = Category(
            name='Cloud & DevOps',
            description='Containerization, CI/CD pipelines, production deployment, and monitoring.'
        )
        cat_career = Category(
            name='Career & Tech Insights',
            description='Navigating software engineering internships, interview tips, and project showcases.'
        )

        db.session.add_all([cat_flask, cat_webdev, cat_ai, cat_devops, cat_career])
        db.session.commit()

        print("Seeding Tags...")
        tag_flask = Tag(name='flask')
        tag_python = Tag(name='python')
        tag_webdev = Tag(name='webdev')
        tag_sqlite = Tag(name='sqlite')
        tag_bootstrap = Tag(name='bootstrap5')
        tag_tutorial = Tag(name='tutorial')
        tag_architecture = Tag(name='architecture')
        tag_security = Tag(name='security')
        tag_fullstack = Tag(name='fullstack')

        db.session.add_all([
            tag_flask, tag_python, tag_webdev, tag_sqlite,
            tag_bootstrap, tag_tutorial, tag_architecture,
            tag_security, tag_fullstack
        ])
        db.session.commit()

        print("Seeding Blog Posts...")
        post1 = Post(
            title='Building Modern Web Applications with Python Flask and Bootstrap 5',
            summary='A comprehensive guide to building responsive, secure, and production-ready web applications using Flask.',
            content='''
            <p>Flask is a lightweight and powerful WSGI web application framework in Python. In this article, we explore how to build a scalable blogging platform with user authentication, SQLAlchemy models, and rich media.</p>
            <h2>Why Choose Flask in 2026?</h2>
            <p>Unlike monolithic frameworks, Flask gives developers granular control over every aspect of their application:</p>
            <ul>
                <li><strong>Micro-framework flexibility:</strong> Include only what you need, from extensions to blueprints.</li>
                <li><strong>Rapid prototyping:</strong> Build and iterate on full-stack MVPs within days.</li>
                <li><strong>Rich Ecosystem:</strong> Flask-SQLAlchemy, Flask-Login, and Flask-WTF make complex workflows effortless.</li>
            </ul>
            <h2>Key Architecture Principles</h2>
            <p>When organizing a production Flask app, always adopt the <em>Application Factory pattern</em>. This isolates configuration and simplifies testing with isolated databases.</p>
            <blockquote>"Simplicity is prerequisite for reliability." – Edsger W. Dijkstra</blockquote>
            <p>Pairing Flask with Bootstrap 5 provides a modern responsive grid, smooth color schemes, and seamless mobile support right out of the box.</p>
            ''',
            author=sarah,
            category=cat_flask,
            views=142
        )
        post1.tags.extend([tag_flask, tag_python, tag_bootstrap, tag_architecture])

        post2 = Post(
            title='Essential Security Practices for Flask: CSRF, Password Hashing, and XSS Protection',
            summary='Master the core security pillars required to shield your Flask apps from common OWASP vulnerabilities.',
            content='''
            <p>Security should never be an afterthought in web development. In this deep dive, we walk through essential defenses every developer must implement.</p>
            <h2>1. Secure Password Hashing with Werkzeug</h2>
            <p>Never store plain passwords! Werkzeug generates salted PBKDF2 or scrypt hashes that resist rainbow table and brute-force attacks.</p>
            <h2>2. CSRF Defense with Flask-WTF</h2>
            <p>Cross-Site Request Forgery is thwarted automatically by attaching cryptographic tokens to every state-changing form submission.</p>
            <h2>3. Content Sanitization Against XSS</h2>
            <p>When allowing rich text input from users, sanitize raw HTML using <code>bleach</code> to strip dangerous <code>&lt;script&gt;</code> tags while keeping safe typography tags.</p>
            ''',
            author=admin,
            category=cat_flask,
            views=215
        )
        post2.tags.extend([tag_flask, tag_security, tag_tutorial])

        post3 = Post(
            title='Mastering Bootstrap 5: Designing Clean, Modern User Interfaces',
            summary='Elevate your UI design with modern color palettes, accessible components, and card layouts.',
            content='''
            <p>Modern web users expect clean typography, responsive layouts, and intuitive navigation. Bootstrap 5 drops jQuery dependencies and embraces CSS custom properties for effortless theming.</p>
            <h2>Design Principles for Engaging Blogs:</h2>
            <ol>
                <li><strong>Visual Hierarchy:</strong> Use distinct heading weights and readable body copy.</li>
                <li><strong>Generous Spacing:</strong> Give cards and articles breathing room with padding and margins.</li>
                <li><strong>Micro-interactions:</strong> Subtle hover states on cards and buttons build a polished experience.</li>
            </ol>
            ''',
            author=alex,
            category=cat_webdev,
            views=89
        )
        post3.tags.extend([tag_bootstrap, tag_webdev, tag_fullstack])

        post4 = Post(
            title='How to Ace Your Python Full-Stack Internship: 8-Week Roadmap',
            summary='Actionable milestones and best practices to transform your internship project into an industry-grade portfolio piece.',
            content='''
            <p>Standing out in software engineering requires more than writing code—it demands clean architecture, disciplined testing, and clear presentation.</p>
            <h2>The 8-Week Blueprint:</h2>
            <ul>
                <li><strong>Week 1-2:</strong> Solidify application foundation, database schemas, and robust authentication.</li>
                <li><strong>Week 3-4:</strong> Complete CRUD workflows, rich-text editing, and intuitive responsive templates.</li>
                <li><strong>Week 5-6:</strong> Implement community discussions, search queries, and dynamic filters.</li>
                <li><strong>Week 7-8:</strong> Write automated test suites, prepare documentation, and record a polished video demonstration.</li>
            </ul>
            ''',
            author=sarah,
            category=cat_career,
            views=310
        )
        post4.tags.extend([tag_tutorial, tag_architecture, tag_fullstack])

        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        print("Seeding Comments...")
        c1 = Comment(
            content='This tutorial laid out the application factory pattern so clearly. Great read!',
            author=alex,
            post=post1
        )
        c2 = Comment(
            content='The security section on bleach sanitization was crucial for our project.',
            author=sarah,
            post=post2
        )
        c3 = Comment(
            content='Following this exact 8-week roadmap for my DIY internship! Highly motivated.',
            author=admin,
            post=post4
        )

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        print("Database seeded successfully with demo content!")

if __name__ == '__main__':
    seed_database()

