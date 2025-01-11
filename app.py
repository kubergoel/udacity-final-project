import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import setup_db, db

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

APP = create_app()

@APP.route('/')
def index():
    return jsonify({
            'success': True
        })
# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)