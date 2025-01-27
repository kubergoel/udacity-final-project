import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import setup_db, db, db_create_all, Movie, Actor, CastingRole
from auth.auth import requires_auth, AuthError
from datetime import datetime
import sys
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
import debugpy


#Code to enable the Debugging of the application
if os.environ.get("FLASK_ENV") == "development" and not debugpy.is_client_connected():
   debugpy.listen(("0.0.0.0", 5780))
   print("Debug mode Enabled")

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
            setup_db(app)
    else:
            database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
            setup_db(app, database_path=database_path)

    return app

app = create_app()

#db_create_all()

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,PUT")
    return response

@app.route('/')
def index():
    print('Success!!')
    return jsonify({
            'success': True,
            'test': 'Hello'
        })

'''
    GET /movies
        Fetches all the available Movies in database
    returns status code 200 and json {"success": True, "movies": movies} where movies is the list of all the movies
        or appropriate status code indicating reason for failure
'''
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.order_by(Movie.creation_time).all()
    if len(movies) == 0:
        abort(404)
    movies_json=[]
    for movie in movies:
        roles = movie.roles
        roles_json = []
        for role in roles:
            roles_json.append(role.to_json())
        movie_json = movie.to_json()
        if roles_json is not None:
            movie_json['roles'] = roles_json
        movies_json.append(movie_json)
    print(movies_json)
    return jsonify({
            'success': True,
            'movies' : movies_json
        })

'''
    GET /movies
        Fetches all the available Movies in database
    returns status code 200 and json {"success": True, "movies": movies} where movies is the list of all the movies
        or appropriate status code indicating reason for failure
'''
@app.route('/movie/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    roles = movie.roles
    roles_json = []
    for role in roles:
        roles_json.append(role.to_json())
    movie_json = movie.to_json()
    if roles_json is not None:
        movie_json['roles'] = roles_json
    print(movie_json)
    return jsonify({
            'success': True,
            'movie' : movie_json
        })

'''
    Method to check if there is a movie with same Title in database.
    If movie exists it will throw 422 ERROR.
'''
def check_movie_title_exists(title):
    movie = Movie.query.filter(Movie.title  == title).one_or_none()
    if movie is not None:
        error_m = "Movie with the title {title} already exists.".format(title=title)
        print(error_m)
        raise UnprocessableEntity(error_m)

'''
    POST /movies
        Saves the movie data in Database
    returns status code 200 and json {"success": True, "movie_id": movie_id} where movie_id is the id of the newly created movie
        or appropriate status code indicating reason for failure
'''
@app.route('/movie', methods=['POST'])
@requires_auth('post:movies')
def add_movies(payload):
    body = request.get_json()
    title = body.get('title', None)
    genre = body.get('genre', None)
    release_date = body.get('release_date', None)
    description = body.get('description', None)
    creation_time = datetime.now()
    check_movie_title_exists(title)
    try:
            movie = Movie(title=title, genre=genre, release_date=release_date, description=description, creation_time=creation_time)    
            movie.add()
            return jsonify({
                    'success': True,
                    'movie_id' : movie.id
                })
    except:
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        #abort(500)
        raise InternalServerError(message)
    

'''
    PATCH /movie/<int:movie_id>
        Update the movie data in Database
    returns status code 200 and json {"success": True} where movie_id is the id of the newly created movie
        or appropriate status code indicating reason for failure
'''
@app.route('/movie/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        title = body.get('title', None)
        genre = body.get('genre', None)
        release_date = body.get('release_date', None)
        description = body.get('description', None)
        last_updated_time = datetime.now()

        if title is not None:
            movie.title = title
        if genre is not None:
            movie.genre = genre
        if release_date is not None:
            movie.release_date = release_date
        if description is not None:
            movie.description = description
        movie.last_updated_time =last_updated_time
        try:
            movie.update()
            return jsonify({
                'success': True
                    })
        except:
            message = "Error : {0}".format(sys.exc_info())
            print(message)
            raise InternalServerError(message)

'''
    DELETE /movie/<int:movie_id>
        Delete the movie data from Database
    returns status code 200 and json {"success": True, "movie_id": movie_id} where movie_id is the id of the movie deleted
        or appropriate status code indicating reason for failure
'''
@app.route('/movie/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)
    try:        
        movie.delete()
        return jsonify({
                'success': True,
                'movie_id': movie_id
            })
    except:
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        raise InternalServerError(message)

'''
    GET /actors
        Fetches all the available Actors in database
    returns status code 200 and json {"success": True, "actors": actors} where actors is the list of all the actors
        or appropriate status code indicating reason for failure
'''
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.order_by(Actor.name).all()
    if len(actors) == 0:
        abort(404)
    actors_json=[]

    for actor in actors:
        roles = actor.roles
        roles_json = []
        for role in roles:
            roles_json.append(role.to_json())
        actor_json = actor.to_json()
        if roles_json is not None:
            actor_json['roles'] = roles_json
        actors_json.append(actor_json)
    print(actors_json)
    return jsonify({
            'success': True,
            'actors' : actors_json
        })

'''
    GET /actor/<int:actor_id>
        Fetches the actor corrsponding to the actor_id
    returns status code 200 and json {"success": True, "actor": actor} 
        or appropriate status code indicating reason for failure
'''
@app.route('/actor/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    actor_json = actor.to_json()
    print(actor_json)
    return jsonify({
            'success': True,
            'actor' : actor_json
        })

'''
    POST /actor
        Saves the actor data in Database
    returns status code 200 and json {"success": True, "actor_id": actor_id} where actor_id is the id of the newly created actor
        or appropriate status code indicating reason for failure
'''
@app.route('/actor', methods=['POST'])
@requires_auth('post:actors')
def add_actors(payload):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    city = body.get('city', None)
    state = body.get('state', None)
    address = body.get('address', None)
    phone = body.get('phone', None)
    image_link = body.get('image_link', None)
    creation_time = datetime.now()
    try:
            actor = Actor(name=name, age=age, gender=gender, city=city, creation_time=creation_time, state=state, address=address, phone=phone, image_link=image_link)
            actor.add()
            return jsonify({
                    'success': True,
                    'actor_id' : actor.id
                })
    except:
        print(sys.exc_info())
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        raise InternalServerError(message)

'''
    PATCH /actor/<int:actor_id>
        Update the movie data in Database
    returns status code 200 and json {"success": True}
        or appropriate status code indicating reason for failure
'''
@app.route('/actor/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        city = body.get('city', None)
        state = body.get('state', None)
        address = body.get('address', None)
        phone = body.get('phone', None)
        image_link = body.get('image_link', None)
        last_updated_time = datetime.now()

        if name is not None:
            actor.name = name
        if age is not None:
            actor.age = age
        if gender is not None:
            actor.gender = gender
        if city is not None:
            actor.city = city
        if state is not None:
            actor.state = state
        if address is not None:
            actor.address = address
        if phone is not None:
            actor.phone = phone
        if image_link is not None:
            actor.image_link = image_link
        actor.last_updated_time =last_updated_time
        try:
            actor.update()
            return jsonify({
                'success': True
                    })
        except:
            message = "Error : {0}".format(sys.exc_info())
            print(message)
            raise InternalServerError(message)

'''
    DELETE /actor/<int:actor_id>
        Delete the actor data from Database
    returns status code 200 and json {"success": True, "actor_id": actor_id} where actor_id is the id of the actor deleted
        or appropriate status code indicating reason for failure
'''
@app.route('/actor/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:        
        actor.delete()
        return jsonify({
                'success': True,
                'actor_id': actor_id
            })
    except:
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        raise InternalServerError(message)

'''
    GET /casting-roles
        Fetches all the available Casting Roles in database
    returns status code 200 and json {"success": True, "casting_roles": casting_roles} where casting_roles is the list of all the Casting Roles
        or appropriate status code indicating reason for failure
'''
@app.route('/casting-roles', methods=['GET'])
@requires_auth('get:castingRoles')
def get_castingRoles(payload):
    casting_roles = CastingRole.query.join(Movie).join(Actor).with_entities(CastingRole.role_id, CastingRole.role_name, CastingRole.is_lead_role, CastingRole.description, CastingRole.movie_id, CastingRole.actor_id, Movie.title, Actor.name).order_by(CastingRole.role_name).all()
    if len(casting_roles) == 0:
        abort(404)
    #for role in casting_roles:
    casting_roles_json = transform_to_json(casting_roles)
    print(casting_roles_json)
    return jsonify({
            'success': True,
            'casting_roles' : casting_roles_json
        })

def transform_to_json(casting_roles):
    casting_roles_json=[]
    
    for role_id, role_name, is_lead_role, description, movie_id, actor_id, title, name in casting_roles:
        casting_roles_json.append( {
            'role_id': role_id,
            'role_name': role_name,
            'is_lead_role': is_lead_role,
            'description': description,
            'movie': title,
            'actor': name
        })
    return casting_roles_json
'''
    POST /casting-role
        Saves the Role data in Database
    returns status code 200 and json {"success": True, "role_id": role_id} where role_id is the id of the newly created role
        or appropriate status code indicating reason for failure
'''
@app.route('/casting-role', methods=['POST'])
@requires_auth('post:castingRoles')
def add_castingRole(payload):
    body = request.get_json()

    role_name = body.get('role_name', None)
    is_lead_role = body.get('is_lead_role', False)
    movie_id = body.get('movie_id', None)
    actor_id = body.get('actor_id', None)
    description = body.get('description', None)
    creation_time = datetime.now()

    validate_actor_and_movie(actor_id, movie_id)

    try:
            casting_role = CastingRole(role_name=role_name, is_lead_role=is_lead_role, description=description, movie_id=movie_id, actor_id=actor_id, creation_time=creation_time)
            casting_role.add()
            return jsonify({
                    'success': True,
                    'role_id' : casting_role.role_id
                })
    except:
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        #abort(500)
        raise InternalServerError(message)

def validate_actor_and_movie(actor_id, movie_id):
    validate_actor(actor_id)
    validate_movie(movie_id)

def validate_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        raise InternalServerError("Either Actor ID is not provided or given Actor ID is not present.")

def validate_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        raise InternalServerError("Either Movie ID is not provided or given Movie ID is not present.")

'''
    PATCH /casting-role/<int:role_id>
        Update the movie data in Database
    returns status code 200 and json {"success": True} where role_id is the id of the role that need to be updated
        or appropriate status code indicating reason for failure
'''
@app.route('/casting-role/<int:role_id>', methods=['PATCH'])
@requires_auth('patch:castingRoles')
def update_role(payload, role_id):
        role = CastingRole.query.filter(CastingRole.role_id == role_id).one_or_none()
        if role is None:
            abort(404)
        body = request.get_json()
        role_name = body.get('role_name', None)
        is_lead_role = body.get('is_lead_role', False)
        movie_id = body.get('movie_id', None)
        actor_id = body.get('actor_id', None)
        description = body.get('description', None)
        last_updated_time = datetime.now()

        if role_name is not None:
            role.role_name = role_name
        if is_lead_role is not None:
            role.is_lead_role = is_lead_role
        if description is not None:
            role.description = description
        if movie_id is not None:
            role.movie_id = movie_id
        if actor_id is not None:
            role.actor_id = actor_id
        role.last_updated_time =last_updated_time

        if movie_id is not None:
            validate_movie(movie_id)
        
        if actor_id is not None:
            validate_actor(actor_id)

        try:
            role.update()
            return jsonify({
                'success': True,
                'role': role.to_json()
                    })
        except:
            message = "Error : {0}".format(sys.exc_info())
            print(message)
            raise InternalServerError(message)

'''
    DELETE /casting-role/<int:role_id>'
        Delete the Role data from Database
    returns status code 200 and json {"success": True, "role_id": role_id} where role_id is the id of the role deleted
        or appropriate status code indicating reason for failure
'''
@app.route('/casting-role/<int:role_id>', methods=['DELETE'])
@requires_auth('delete:castingRoles')
def delete_castingRole(payload, role_id):
    
    role = CastingRole.query.filter(CastingRole.role_id == role_id).one_or_none()
    if role is None:
        abort(404)
    try:        
        role.delete()
        return jsonify({
                'success': True,
                'role_id': role_id
            })
    except:
        message = "Error : {0}".format(sys.exc_info())
        print(message)
        raise InternalServerError(message)

@app.route('/casting-roles/movie/<int:movie_id>', methods=['GET'])
@requires_auth('get:castingRoles')
def get_movie_roles(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    roles = movie.roles
    roles_json = []
    for role in roles:
        roles_json.append(role.to_json())
    return jsonify({
        'success': True,
        'movie': movie.to_json(),
        'roles': roles_json
    })

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": 'The request is Unprocessable'
    }), 422

@app.errorhandler(404)
def not_found(error):
        return (jsonify({
            'success': False,
            'error': 404,
            'message': 'The object is Not Found'
        }), 404)
    
@app.errorhandler(401)
def unauthorized(error):
        return (jsonify({
            "success": False, 
            "error": 401, 
            "message": "The request is Unauthorized"}),
            401)

@app.errorhandler(403)
def unauthenticated(error):
        return (jsonify({
            "success": False, 
            "error": 403, 
            "message": "Request is Unauthenticated"}),
            403)
    
@app.errorhandler(400)
def request_unprocessable(error):
        return (jsonify({
            "success": False, 
            "error": 400, 
            "message": "Unable to process the Request"}),
            400)
    
@app.errorhandler(500)
def internal_server_error(error):
        return (jsonify({
            "success": False, 
            "error": 500, 
            "message": "Internal Server Error",
            "description": error.description}),
            500)

@app.errorhandler(AuthError)
def auth_error_Handler(error):
        return (jsonify(
            error.error),
            error.status_code)

@app.errorhandler(InternalServerError)
def handle_internal_error(error):
    response = jsonify({
        "error": "Internal Server Error1",
        "message": error.description
    })
    response.status_code = 500
    return response


@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(error):
    response = jsonify({
        "error": "Request cannot be Processed",
        "message": error.description
    })
    response.status_code = 422
    return response
