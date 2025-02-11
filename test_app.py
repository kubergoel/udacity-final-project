import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import db, Movie, Actor, CastingRole
from database.db_settings import TEST_DATABASE_URL
import pytest
from datetime import datetime

# TEST CASE CLASS


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = TEST_DATABASE_URL
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2EzYTNkMjlhNDljNGRmZjMyOTkxMTMiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3MzkxODg3MDMsImV4cCI6MTczOTI3NTA3NCwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyJdfQ.AsMO05j0j34ZLDB5NWrG2ozJIdfY40_5SlGUzwBhXzX6Yg3jMVBtlV2r9eD7_Xy1l17PfxYhRxYjJE2wULqjIB5GYI6KyGIPb9T9i2yt6xN4lVRBMpe6aXhr9urbjvqWSuoCCZonWhF_z4r61DzeO0KjHex79Y4mDaUYgwGywQuDm82I1zJknhNBuK8PEp8eKK90kkrn0LEr4NgCMb7MRQ-BkXhKFaIMSjT_waDqPDPTx41jtFIN-CTwsIrRVDP3JY-S5OEZv26Bi17wjFqQIqcrQN4JHcDg3_yvkpRZaHxwgB2OSwP8XIVaTmyzhC2fFu7TcFqkeiU6me3WcJNtBA'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2EzYTM5OWViNjhmZTkyZWIzZjZmZDEiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3MzkxODg2NDQsImV4cCI6MTczOTI3NTAxNSwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0OmNhc3RpbmdSb2xlcyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDpjYXN0aW5nUm9sZXMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.P5XefvLQt5fEADVVFnaeDqW1BXGNjqRLFLZ-qVPV6ExHY3TNm34xpB2KkO5OZbUeoc6WLKLfGy3gbhoo8G3xMzItnF2QY4lViuh4JTbPy3wJYELSFqX-eBS_hTYWYzSIRrkF8uD-Z31DM7YX_2SWGpYmHp7drpcn6SzC0qMpHAdKXO9N6PzzWl59GtagQU7yATNG3Va_fzvl1WV1XVLQ6Mh1SATsUatPDCQFKl8QKjsJFXWGpypzwL3DAm4uyxujIi02fdSCAWoHX_UpGpsU3ZCnARAOIyYrEkWpqI0mr6nC8Vl9u7m0nyXnmtjdZLE2kEgUzf8KltFxCGG4BrhTsQ'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2EzYTJlZmViNDY0NWI2Yjg2ZDc4ZTgiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3MzkxODg4MDAsImV4cCI6MTczOTI3NTE3MSwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ1JvbGVzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOmNhc3RpbmdSb2xlcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5nUm9sZXMiLCJwb3N0Om1vdmllcyJdfQ.Qk-3hFz6cpLIXt26Lsrcsc8_YqNNqJvXRilTrWjQ_FbwrGYiKnAeLvChn0DQJd2iMv50rVjvpLaM-BbhKLUgdWFEKzglHfwkSgatAzX8mfI7V237SAc9vHF4rqAqGKbCAMk-SXWH_6VXbRK2LovMkCRcgqhWLleFtyQBcqbzBTqkyDoXXeAhKI_hLkQxJdqLB62mc9n-rdbwuxtOWmLHAhCcnaHZHn4L_LaxFlBD4RV9fLYJmkw_rTj2llxtjANMtFPsvcDZPcCxW5JASMvBCiPdmYWPWvY_HiQSo5C2en6l4QPICm-FczMiXSvircammwDtsL6mJc5Le62CmI9Ayg'
        EXPIRED_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2EzYTNkMjlhNDljNGRmZjMyOTkxMTMiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3Mzg4NjM5MDAsImV4cCI6MTczODk1MDI3MSwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyJdfQ.Ju05aSNBFUmOQRk_Mwl5JTLCgHFnqBbLQ-TXQAmF32VIISr3-qw_29NhJyA-pJl2c1KMyuJSHzl-Uv8dpxxa946wFKqj08m1hQO1sZiOvkSu-o3wkx6VgPafoAiCVSswxJFYfUiS9XY96BjZii9AjBZfU6gMtkd0I_nNPJp2pVD052C-HNHOPA_OGJGXg4f2TY1y9u9619O9h_jqO3qognKItX4c_vNtR67RryV9CekjRq4zaMFWrmo-ECG25LlkeA3-Oaiu-MhoYB1buzo4Tgtesc-i3XR2w-KRKJtNB_B5dnL2HveZU1ce5iDKJ2Fhivnqj8E4x3mK3mzTGQ4uAg'
        INCORRECT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2EzYTNkMjlhNDljNGRmZjMyOTkxMTMiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3Mzg4NjM5MDAsImV4cCI6MTczODk1MDI3MSwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyJdfQ.Ju05aSNBFUmOQRk_Mwl5JTLCgHFnqBbLQ-TXQAmF32VIISr3-qw_29NhJyA-pJl2c1KMyuJSHzl-Uv8dpxxa946wFKqj08m1hQO1sZiOvkSu-o3wkx6VgPafoAiCVSswxJFYfUiS9XY96BjZii9AjBZfU6gMtkd0I_nNPJp2pVD052C-HNHOPA_OGJGXg4f2TY1y9u9619O9h_jqO3qognKItX4c_vNtR67RryV9CekjRq4zaMFWrmo-ECG25LlkeA3-Oaiu-MhoYB1buzo4Tgtesc-i3XR2w-KRKJtNB_B5dnL2HveZU1ce5iDKJ2Fhivnqj8E4x3mK3mzTGQ4uAgh'

        self.assistant_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}
        self.expired_header = {'Authorization':
                                     'Bearer ' + EXPIRED_TOKEN}
        self.incorrect_header = {'Authorization':
                                     'Bearer ' + INCORRECT_TOKEN}
        
        self.app = create_app({
            'SQLALCHEMY_DATABASE_URI': DATABASE_URL,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            "TESTING": True
        })
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.db = db
        self.db.create_all()

        self.movie = Movie(title='Test Title', genre='Test Genre', release_date='2025-10-10', description='Test Description', creation_time=datetime.now())
        self.movie.add()
        movie_obj = Movie.query.filter(Movie.title == 'Test Title').first()

        self.actor = Actor(name='Test', age=20, gender='Male', city='Test', creation_time=datetime.now(), state='Test', address='Test', phone='9999999999')
        self.actor.add()
        actor_obj = Actor.query.filter(Actor.name == 'Test').first()

        casting_role = CastingRole(role_name='Test', is_lead_role=True, description='Test', movie_id=movie_obj.id, actor_id=actor_obj.id, creation_time=datetime.now())
        casting_role.add()

        self.movie_to_post = Movie(title='Test Title1', genre='Test Genre1', release_date='2025-10-10', description='Test Description1', creation_time=datetime.now())
        self.actor_to_post = Actor(name='Test1', age=20, gender='Male', city='Test', creation_time=datetime.now(), state='Test', address='Test', phone='9999999999')
    def tearDown(self):
        """Cleanup after each test."""
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
        #pass

    def test_get_movies1(self):
        """Test GET Movies API for Success for Casting Assistant Token"""
        res = self.client().get('/movies', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies2(self):
        """Test GET Movies API for Success for Casting Director Token"""
        res = self.client().get('/movies', headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies3(self):
        """Test GET Movies API for Success for Executive Producer Token"""
        res = self.client().get('/movies', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies4(self):
        """Test GET Movies API for Failure for Expired Token"""
        res = self.client().get('/movies', headers=self.expired_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'token_expired')

    def test_get_movie(self):
        """Test GET Movie API for Success for a given Movie ID"""
        movie = Movie.query.filter(Movie.title == 'Test Title').first()
        res = self.client().get('/movie/{}'.format(movie.id), headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], 'Test Title')

    def test_post_movie(self):
        """Test Post Movie API for Success for a given Movie Object"""
        res = self.client().post('/movie', json=self.movie_to_post.to_json(), headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie_id'] > 0)
       
    def test_post_movie1(self):
        """Test Post Movie API for Failure for Duplicate Object"""
        res = self.client().post('/movie', json=self.movie.to_json(), headers=self.producer_header)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Movie with the title Test Title already exists.')

    def test_post_movie2(self):
        """Test Post Movie API for Authorization Failure for a given Movie Object"""
        movie = Movie.query.filter(Movie.title == 'Test Title').first()
        res = self.client().post('/movie', json=self.movie.to_json(), headers=self.director_header)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 403)
        

    def test_patch_movie1(self):
        """Test Patch Movie API for Success for a given Movie Object"""
        movie = Movie.query.filter(Movie.title == 'Test Title').first()
        print(movie)
        movie.description = 'New Description'
        res = self.client().patch('/movie/{}'.format(movie.id), json=self.movie.to_json(), headers=self.director_header)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie1(self):
        """Test Delete Movie API for Success for a given Movie Object"""
        movie = Movie(title='Test Title Delete', genre='Test Genre', release_date='2025-10-10', description='Test Description', creation_time=datetime.now())
        movie.add()
        print(movie)
        res = self.client().delete('/movie/{}'.format(movie.id), headers=self.producer_header)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie2(self):
        """Test Delete Movie API for Failure due to Authorization Error"""
        movie = Movie(title='Test Title', genre='Test Genre', release_date='2025-10-10', description='Test Description', creation_time=datetime.now())
        movie.add()
        print(movie)
        res = self.client().delete('/movie/{}'.format(movie.id), headers=self.director_header)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 403)
    
    def test_get_actors1(self):
        """Test GET Actors API for Success for Casting Assistant Token"""
        res = self.client().get('/actors', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)
        
    
    def test_get_actors2(self):
        """Test GET Actors API for Failure for Incorrect Token"""
        res = self.client().get('/actors', headers=self.incorrect_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['code'], 'invalid_header')

    def test_post_actor(self):
        """Test Post Actor API for Success for a given Actor Object"""
        res = self.client().post('/actor', json=self.actor_to_post.to_json(), headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor_id'] > 0)

    def test_patch_actor(self):
        """Test Patch Actor API for Success for a given Actor Object"""
        actor = Actor.query.filter(Actor.name == 'Test').first()
        print(actor)
        actor.age = 29
        res = self.client().patch('/actor/{}'.format(actor.id), json=self.actor.to_json(), headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_actor(self):
        """Test Delete Actor API for Success for a given Actor Object"""
        actor = Actor(name='Test Delete', age=20, gender='Male', city='Test', creation_time=datetime.now(), state='Test', address='Test', phone='9999999999')
        actor.add()
        print(actor)
        res = self.client().delete('/actor/{}'.format(actor.id), headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_casting_roles(self):
        """Test GET Casting Roles API for Success for Casting Assistant Token"""
        res = self.client().get('/casting-roles', headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['casting_roles']) > 0)
        print('Casting Role : ',data['casting_roles'][0])
        self.assertEqual(data['casting_roles'][0]['actor'], 'Test')
        self.assertEqual(data['casting_roles'][0]['movie'], 'Test Title')

if __name__ == "__main__":
    unittest.main()
    