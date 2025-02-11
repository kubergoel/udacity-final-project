import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from .db_settings import DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS



db = SQLAlchemy()

def setup_db(app, database_path=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

def db_create_all():
    with db.app.app_context():
         db.create_all()
    print('Hello')

#Actors, Movies

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50))
    release_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    creation_time = db.Column(db.DateTime, nullable=False)
    last_updated_time = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'release_date': self.release_date,
            'description': self.description
        }
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
      return f'<Movie ID: {self.id}, Movie Title: {self.title}>'

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    creation_time = db.Column(db.DateTime, nullable=False)
    last_updated_time = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link
        }

    def add(self):
            db.session.add(self)
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
      return f'<Actor ID: {self.id}, Actor Name: {self.name}>'

class CastingRole(db.Model):
    __tablename__ = 'casting_role'
    
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(120), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    is_lead_role = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200))
    movie = db.relationship('Movie', backref=db.backref('roles', lazy=True))
    artist = db.relationship('Actor', backref=db.backref('roles', lazy=True))
    creation_time = db.Column(db.DateTime, nullable=False)
    last_updated_time = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'is_lead_role': self.is_lead_role,
            'description': self.description
        }
    
    def add(self):
            db.session.add(self)
            db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
    def __repr__(self):
      return f'<Role ID: {self.role_id}, Role Name: {self.role_name}>'
      