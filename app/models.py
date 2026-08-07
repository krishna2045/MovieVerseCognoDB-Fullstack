import sqlite3
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    """User model supporting both Neo4j/CognoDB and SQLite (mqlslite) storage."""
    def __init__(self, data):
        if hasattr(data, 'get'):
            self.id = data.get('username') or getattr(data, 'id', None)
            self.username = data.get('username')
            self.email = data.get('email')
            self.password_hash = data.get('password_hash')
            self.created_at = str(data.get('created_at', ''))
        elif isinstance(data, dict):
            self.id = data.get('username') or data.get('id')
            self.username = data.get('username')
            self.email = data.get('email')
            self.password_hash = data.get('password_hash')
            self.created_at = str(data.get('created_at', ''))
        else:
            self.id = str(getattr(data, 'id', ''))
            self.username = getattr(data, 'username', 'Cinephile')
            self.email = getattr(data, 'email', '')
            self.password_hash = getattr(data, 'password_hash', '')
            self.created_at = ''

    def get_id(self):
        return str(self.username)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def create(driver, username, email, password_hash):
        # 1. Try creating in SQLite
        try:
            conn = sqlite3.connect("movieverse.db")
            c = conn.cursor()
            c.execute(
                "INSERT OR REPLACE INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("SQLite User creation warning:", e)

        # 2. Try creating in Neo4j
        if driver:
            try:
                with driver.session() as session:
                    result = session.run(
                        """
                        MERGE (u:User {username: $username})
                        SET u.email = $email, u.password_hash = $pwd, u.created_at = datetime()
                        RETURN u
                        """,
                        username=username,
                        email=email,
                        pwd=password_hash,
                    )
                    record = result.single()
                    if record and record.get('u'):
                        return User(record['u'])
            except Exception as e:
                print("Neo4j User creation warning:", e)

        return User({'username': username, 'email': email, 'password_hash': password_hash})

    @staticmethod
    def find_by_username(driver, username):
        if not username:
            return None

        # Try Neo4j first
        if driver:
            try:
                with driver.session() as session:
                    result = session.run(
                        """
                        MATCH (u:User)
                        WHERE toLower(u.username) = toLower($identifier) OR toLower(u.email) = toLower($identifier)
                        RETURN u LIMIT 1
                        """,
                        identifier=username.strip(),
                    )
                    record = result.single()
                    if record and record.get('u'):
                        return User(record['u'])
            except Exception as e:
                print("Neo4j find_by_username exception:", e)

        # SQLite Fallback / Dual lookup
        try:
            conn = sqlite3.connect("movieverse.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                "SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?) LIMIT 1",
                (username.strip(), username.strip())
            )
            row = c.fetchone()
            conn.close()
            if row:
                return User(dict(row))
        except Exception as e:
            print("SQLite find_by_username exception:", e)

        return None

    @staticmethod
    def find_by_id(driver, user_id):
        if not user_id:
            return None
        return User.find_by_username(driver, str(user_id))
