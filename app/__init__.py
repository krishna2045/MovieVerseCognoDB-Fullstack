from flask import Flask
from .config import DevelopmentConfig as Config
from .extensions import neo4j_driver
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    # Load configuration
    app.config.from_object(Config)
    # Initialize extensions
    from .extensions import neo4j_driver, login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    # Initialize Neo4j driver
    neo4j_driver.init_app(app)
    # Import auth routes to ensure they are registered with the blueprint
    from .auth import routes as auth_routes

    # Register blueprints
    app.register_blueprint(main_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # Context processors
    @app.context_processor
    def inject_globals():
        return dict(current_year=2026)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return ("<h1>404 – Not Found</h1><p>The page you are looking for does not exist.</p>", 404)

    @app.errorhandler(500)
    def server_error(e):
        return ("<h1>500 – Server Error</h1><p>Something went wrong. Please try again later.</p>", 500)

    return app
