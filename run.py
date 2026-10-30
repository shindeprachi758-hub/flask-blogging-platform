import os
from app import create_app
from app.extensions import db
from app.models import User, Post, Category, Tag, Comment

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell."""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment
    }


@app.cli.command('init-db')
def init_db():
    """Initialize database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables initialized successfully.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)

