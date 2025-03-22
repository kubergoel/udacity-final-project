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
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Nzg5NGVkOGFhZDc1M2U2YWZjZDYxMDciLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3NDI2MzcyODEsImV4cCI6MTc0MjcyMzY1Miwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyJdfQ.T3cncNES7vu4N3V1ouFj1oiL4IrQ4D9AeFLKUkuxfHSZ82Z3u5T-tA6xay9R-0gelQ6Ev2kll2kv8JgJRYUbosJ2_P4CukG-W-9vvC97W7ZQocGCzuU2gh_Jpu9y-YYNyk8qDqhpZTClzxZ9iSkqMOwNOqkO6-WB2kq2rOZoXcJp0YkPvAzLyAA5aAUZQwZe3CBHxaIqRohcF5mafVZRBynaHzusN3KDoylZM03wPIpVscuWsVq1NjnmipRy1G8WdH9kJQaNGrshRCOcVKa0QGXCHKIaztVwbo4r2QOlih0zlbLwY_QtBcS9Zia-RCQ86tO8uUzCVoxX21O7RSiz-g'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Nzg5NGYyM2FiNDAwNzk5ODgzMzA1ODAiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3NDI2MzczOTEsImV4cCI6MTc0MjcyMzc2Miwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0OmNhc3RpbmdSb2xlcyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDpjYXN0aW5nUm9sZXMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.KwQ2dufNvDwp97Pgau-m9QPir_r8t69p8D8Q9nYE55Fy_lbaAk7pt5fwUcZ88mtP8-zmp7HwI8BSN7ocuVv7-CH25zlR-S_oy5jIbt-ge2VZLUCG7L5MQgT-dCftAHvZqcAr3cZ-SM9G9ohqdRAWMF_M4AyMhXfzcNtr5FDwYWtpmprCqvnnsOcRUFx7NBIaKEcXJjWKaTzBoIvqY-ebWG9yXyR5Hg3v-_-7_KEiWhC3o9Eo_knfpPTwY34fbFmfzscF0LeHrYDcBEvchHpDHUFJi0VqW2fpSSpt_9zBBCrsiWQMKU8kRdHvDAuTL6PrHwS1z3zOqdYwIpG_pU356Q'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjlHZjBQTTVxcDJfNnBwSkt3NGJGOSJ9.eyJpc3MiOiJodHRwczovL2Rldi1peWF1azJhdTFhbnJ4Z3M3LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Nzg5NTNlMzQ5NjFhOTJhYmM0MTllZWMiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeS1hcGkiLCJpYXQiOjE3NDI2Mzc0NzksImV4cCI6MTc0MjcyMzg1MCwic2NvcGUiOiIiLCJhenAiOiJMTGxoWEdFZDZOYUhQTFlid0x4ZFhRcDhNNzBtSUxFdCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ1JvbGVzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ1JvbGVzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOmNhc3RpbmdSb2xlcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5nUm9sZXMiLCJwb3N0Om1vdmllcyJdfQ.CjQwZ9Lr2ELlIvTONEDVLsNf9PwZuIltiJRUPU-JYxJhpdQLgivFu1__MPZKfsCZrqyf-N7xy6MzILSE19u6j5XIxJRc9JUXZvZAkAsOq5wIZRRO0uFjTxmVvhZgZ5CeSKi2qOV4yr2vByJ7qKTszqidZmZRnRbremIohfnAVEHUPl-GOXSofOrrfNAS03jPXGkjHU1_goHmCJ74VaodysHM9aGUAMevx4vh35Z6_GMOJnAiJUGn8YinNXFzj6WivPdSPf6kK6sB7r7GqaRs7lXC_hK6WWGnrnmMhurNedZIxFS37atZF_ndxWHuDdcy9VZOc0EzB7CMni3Nx2YwIQ'
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
    