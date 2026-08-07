from neo4j import GraphDatabase
from flask import current_app
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Load user from Neo4j driver or SQLite database using user ID."""
    from flask import current_app
    from .models import User
    driver = current_app.extensions.get('neo4j')
    return User.find_by_id(driver, user_id)

class Neo4jDriver:
    def __init__(self):
        self.driver = None

    def init_app(self, app):
        uri = app.config.get('COGNODB_URI')
        user = app.config.get('COGNODB_USERNAME')
        password = app.config.get('COGNODB_PASSWORD')
        if not all([uri, user, password]):
            print('Cognodb configuration missing or incomplete. Using SQLite fallback for models.')
            return

        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password), max_connection_pool_size=50)
            app.extensions['neo4j'] = self.driver
        except Exception as e:
            print("Failed to initialize Neo4j driver:", e)

    def get_session(self):
        if self.driver is None:
            raise RuntimeError('Neo4j driver not initialized')
        return self.driver.session()

# Instantiate a singleton that can be imported elsewhere
neo4j_driver = Neo4jDriver()
