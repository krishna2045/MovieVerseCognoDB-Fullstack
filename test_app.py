import os
import unittest
from app import create_app

class MovieVerseTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['SECRET_KEY'] = 'test-secret-key'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_unauthenticated_redirect(self):
        """Test that unauthenticated users are redirected to /auth/login for protected routes."""
        protected_routes = ['/', '/search', '/recommendations', '/graph', '/about', '/profile']
        for route in protected_routes:
            response = self.client.get(route, follow_redirects=False)
            self.assertEqual(response.status_code, 302, f"Route {route} did not redirect!")
            self.assertIn('/auth/login', response.headers['Location'], f"Route {route} did not redirect to login!")

    def test_login_and_dashboard_access(self):
        """Test login with demo user and access to protected routes."""
        # 1. GET Login Page
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MovieVerse', response.data)
        self.assertIn(b'Loading your cinematic experience', response.data)

        # 2. POST Login with valid credentials
        login_res = self.client.post('/auth/login', data={'username': 'demo', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        
        # 3. Access Dashboard pages after login
        home_res = self.client.get('/')
        self.assertEqual(home_res.status_code, 200)
        self.assertIn(b'Welcome to', home_res.data)
        self.assertIn(b'Popular Movies', home_res.data)
        self.assertIn(b'My Profile', home_res.data)
        self.assertIn(b'Logout', home_res.data)

        search_res = self.client.get('/search?movie=Inception')
        self.assertEqual(search_res.status_code, 200)
        self.assertIn(b'Search Results', search_res.data)

        recs_res = self.client.get('/recommendations')
        self.assertEqual(recs_res.status_code, 200)
        self.assertIn(b'Recommended For You', recs_res.data)

        graph_res = self.client.get('/graph')
        self.assertEqual(graph_res.status_code, 200)
        self.assertIn(b'Knowledge Graph', graph_res.data)

        about_res = self.client.get('/about')
        self.assertEqual(about_res.status_code, 200)
        self.assertIn(b'About', about_res.data)

        profile_res = self.client.get('/profile')
        self.assertEqual(profile_res.status_code, 200)
        self.assertIn(b'Favorite Movies', profile_res.data)

    def test_logout_behavior(self):
        """Test logout destroys session and prevents browser caching."""
        self.client.post('/auth/login', data={'username': 'demo', 'password': 'password123'}, follow_redirects=True)
        logout_res = self.client.get('/auth/logout', follow_redirects=False)
        self.assertEqual(logout_res.status_code, 302)
        self.assertIn('/auth/login', logout_res.headers['Location'])
        self.assertIn('no-cache', logout_res.headers.get('Cache-Control', ''))

        # Verify access is blocked again after logout
        home_after_logout = self.client.get('/', follow_redirects=False)
        self.assertEqual(home_after_logout.status_code, 302)

if __name__ == '__main__':
    unittest.main()
