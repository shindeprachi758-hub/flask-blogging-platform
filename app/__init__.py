import os
from datetime import datetime, timezone
from flask import Flask, render_template
from config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    """Application factory for the Blogging Platform."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # Ensure instance folder exists for SQLite database storage
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.comments import comments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)

    # Context processors for global template data
    @app.context_processor
    def inject_global_data():
        from app.models import Category
        # Avoid database query if tables are not yet created
        try:
            categories = Category.query.order_by(Category.name).all()
        except Exception:
            categories = []
        return {
            'nav_categories': categories,
            'current_year': datetime.now(timezone.utc).year
        }

    # Template filters
    @app.template_filter('format_date')
    def format_date(value, format_str='%b %d, %Y'):
        if value is None:
            return ''
        return value.strftime(format_str)

    @app.template_filter('striptags')
    def striptags_filter(value):
        import re
        if not value:
            return ''
        clean = re.sub(r'<[^>]+>', ' ', value)
        return ' '.join(clean.split())

    # Error handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

