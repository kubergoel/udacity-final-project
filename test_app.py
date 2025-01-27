
import os
import unittest
import json
from unittest.mock import patch
import pdb

from app import create_app
from database.models import db, Movie, Actor
from database.db_settings import TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD, DB_HOST, DB_PORT


class CastingAgencyTest(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()
        self.obj = Movie(title='Test Movie', genre='Test Genre', release_date='2025-12-21', description='Test Description', creation_time='2025-01-26')
        self.new_movie = self.obj.to_json()
        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            movie_insert = Movie.query.filter(Movie.title == 'Test Movie').one_or_none()
            if movie_insert is None:
                movie_insert = Movie(title='Test Movie', genre='Test Genre', release_date='2025-12-21', description='Test Description', creation_time='2025-01-26')
                movie_insert.add()
            # question_delete = Question.query.filter(Question.question == self.new_question['question']).one_or_none()
            # if question_delete is not None:
            #      question_delete.delete()
      #      db.session.remove()
      #      db.drop_all()

    # """
    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    # """
    # def test_get_movies(self):
    #      """Test GET Movies API for Success"""
    #      print("Starting test_example")
    #      print(f"Self : {self}")
    #      res = self.client.get('/movies')
         
    #      print(f"Response data: {res.data}")
    #      data = json.loads(res.data)
    #      self.assertEqual(res.status_code, 200)
    #      self.assertTrue(data['movies'])
    #      self.assertEqual(len(data['movies']), 1)

    @patch('app.requires_auth')  # Mock the requires_auth decorator
    def test_get_movies_success(self, mock_requires_auth):
        mock_requires_auth.return_value = lambda f: f  # Bypass the decorator
        pdb.set_trace() 
        with self.app.app_context():
            # Mock the database query
            with patch('app.Movie.query.order_by') as mock_query:
                    mock_query.return_value.all.return_value = self.obj
                    print("Starting test_example")
                    print(f"Client :  {self.client}")
                    response = self.client.get('/movies')
                    print(f"Response data: {response.data}")
                    data = response.get_json()

                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(data['success'])
                    self.assertEqual(len(data['movies']), 1)
                    self.assertEqual(data['movies'][0]['title'], "Test Movie")


    # def test_fetch_questions(self):
    #      """Test GET Questions API for Success"""
    #      res = self.client.get('/actors')
    #      data = json.loads(res.data)
    #      self.assertEqual(res.status_code, 200)
    #      self.assertTrue(data['questions'])
    #      self.assertEqual(len(data['questions']), 10)    
    #      self.assertEqual(data['total_questions'], 19)

    # def test_fetch_paginated_questions(self):
    #         """Test GET Paginated Questions API for Success"""
    #         res = self.client.get('/questions?page=2')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 200)
    #         self.assertTrue(data['questions'])
    #         self.assertEqual(len(data['questions']), 9) 
    
    # def test_404_fetch_paginated_questions(self):
    #         """Test GET Questions API for Success"""
    #         res = self.client.get('/questions?page=200')
    #         data = json.loads(res.data)
    #         self.assertEqual(res.status_code, 404)
    #         self.assertFalse(data['success'])
    #         self.assertEqual(data['message'], 'Object is Not Found')

    # def test_delete_questions(self):
    #     """Test Delete Questions API for Success"""
    #     with self.app.app_context():
    #         question = Question.query.filter(Question.question == 'Who invented Peanut Butter?').one_or_none()
    #     id = question.id
    #     res = self.client.delete(f"/questions/{id}")
    #     data = json.loads(res.data)
    #     with self.app.app_context():
    #         question = Question.query.filter(Question.id == id).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["question_id"], id)
    #     self.assertEqual(question, None)

    # def test_500_delete_questions(self):
    #     """Test Delete Question API for Failure"""
    #     res = self.client.delete(f"/questions/10000")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 500)
    #     self.assertFalse(data['success'])
    #     self.assertEqual(data['message'], 'Internal Server Error')
    
    # def test_create_new_question(self):
    #     """Test Create Question API for Success"""
    #     res = self.client.post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question_id"])

    # def test_405_if_question_creation_not_allowed(self):
    #     res = self.client.post("/questions/100", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Method is Not Allowed")
    
    # def test_search_question_with_valid_search_term(self):
    #     """Test Search Question with Valid Search Term API for Success"""
    #     res = self.client.post("/questions/search", json={'searchTerm':'What'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["questions"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(data["total_questions"], 8)
    #     self.assertTrue(data["current_category"])

    # def test_search_question_with_invalid_search_term(self):
    #     """Test Search Question with Invalid Search Term API for Success"""
    #     res = self.client.post("/questions/search", json={'searchTerm':'asdsda'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)

    # def test_search_question_with_empty_search_term(self):
    #     """Test Search Question with Invalid Search Term API for Success"""
    #     res = self.client.post("/questions/search", json={'searchTerm':''})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["questions"])
    #     self.assertEqual(len(data["questions"]), 19)
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(data["total_questions"], 19)
    #     self.assertTrue(data["current_category"])

    # def test_questions_for_given_category(self):
    #     """Test Questions for Given Category API for Success"""
    #     res = self.client.get("/categories/2/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["questions"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(data["total_questions"], 4)
    #     self.assertTrue(data["current_category"])

    # def test_questions_for_unknown_category(self):
    #     """Test Questions for Unknown Category API for Failure"""
    #     res = self.client.get("/categories/20/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    
    # def test_quizzes_for_given_category(self):
    #     """Test Quiz for Given Category API for Success"""
    #     res = self.client.post("/quizzes", json={'previous_questions': [2,4,7,9], 'quiz_category': '3'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])

    # def test_quizzes_for_given_category_for_empty_previous_question(self):
    #     """Test Quiz for Given Category API for Success for Previous Question as Empty"""
    #     res = self.client.post("/quizzes", json={'previous_questions': [], 'quiz_category': '3'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])

    # def test_quizzes_for_given_category_for_All_question(self):
    #     """Test Quiz for Given Category API for Success for Quiz Category as 0 which is sent for ALL"""
    #     res = self.client.post("/quizzes", json={'quiz_category': 0})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
