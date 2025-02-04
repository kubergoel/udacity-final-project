import unittest
from unittest.mock import patch
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from database.models import db, Movie, Actor, CastingRole
from datetime import datetime
from database.db_settings import TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD, DB_HOST, DB_PORT
import pytest

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and test environment."""
        # Setup the app for testing with test configuration
        self.app = create_app({
            'SQLALCHEMY_DATABASE_URI': f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}",
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Setup database (in-memory DB for tests)
        self.db = db
        self.db.create_all()
    
    def tearDown(self):
        """Cleanup after each test."""
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    @patch('app.requires_auth')
    def test_protected_route(self, mock_auth):
        """Test a protected route with mocked authentication."""
        mock_auth.return_value = lambda f: f 
        response = self.client.get('/movies')
        print(f"Response status code: {response.status_code}")  # Debugging output
        print(f"Response data: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
