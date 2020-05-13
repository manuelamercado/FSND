import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from flask_migrate import Migrate

from database.models import db, setup_db, Actor, Movie, movies
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate = Migrate(app, db)
  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  ## ROUTES
  @app.route('/')
  def index():
    return "This is the default index of Casting Agency Api Project."

  '''
  GET /actors
    it should be an endpoint accesible for all roles
  returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
    or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=['GET'])
  def retrieve_all_actors():
    actors_data = Drink.query.order_by(Actor.id).all()
    actors = [actor.format() for actor in actorss_data]

    if len(actors_data):
      return jsonify({
        'success': True,
        'drinks': actors
      })
    else:
      abort(404)

  '''
  @TODO implement endpoint
      GET /drinks-detail
          it should require the 'get:drinks-detail' permission
          it should contain the drink.long() data representation
      returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
          or appropriate status code indicating reason for failure
  '''
  @app.route('/drinks-detail', methods=['GET'])
  @requires_auth('get:drinks-detail')
  def retrieve_all_drinks_detail(jwt):
    if jwt:
      drinks_data = Drink.query.order_by(Drink.id).all()
      drinks = [drink.long() for drink in drinks_data]

      if len(drinks_data):
        return jsonify({
          'success': True,
          'drinks': drinks
        })
      else:
        abort(404)
    else:
      abort(401)

  '''
  @TODO implement endpoint
      POST /drinks
          it should create a new row in the drinks table
          it should require the 'post:drinks' permission
          it should contain the drink.long() data representation
      returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
          or appropriate status code indicating reason for failure
  '''
  @app.route('/drinks', methods=['POST'])
  @requires_auth('post:drinks')
  def add_drink(jwt):
    if jwt:
      body = request.get_json()

      new_title = body.get('title', None)
      new_recipe = body.get('recipe', None)

      try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()

        return jsonify({
          'success': True,
          'drinks': [drink.long()],
        })

      except:
        print(sys.exc_info())
        abort(422)
    else:
      abort(401)

  '''
  @TODO implement endpoint
      PATCH /drinks/<id>
          where <id> is the existing model id
          it should respond with a 404 error if <id> is not found
          it should update the corresponding row for <id>
          it should require the 'patch:drinks' permission
          it should contain the drink.long() data representation
      returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
          or appropriate status code indicating reason for failure
  '''
  @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
  @requires_auth('patch:drinks')
  def update_drink(jwt, drink_id):
    if jwt:
      body = request.get_json()

      try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
          abort(404)

        if 'title' in body:
          drink.title = body.get('title', None)
        
        if 'recipe' in body:
          drink.recipe = json.dumps(body.get('recipe', None))
        
        drink.update()

        return jsonify({
          'success': True,
          'drinks': [drink.long()]
        })

      except:
        print(sys.exc_info())
        abort(400)
    else:
      abort(401)

  '''
  @TODO implement endpoint
      DELETE /drinks/<id>
          where <id> is the existing model id
          it should respond with a 404 error if <id> is not found
          it should delete the corresponding row for <id>
          it should require the 'delete:drinks' permission
      returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
          or appropriate status code indicating reason for failure
  '''
  @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
  @requires_auth('delete:drinks')
  def delete_drink(jwt, drink_id):
    if jwt:
      try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
          abort(404)

        drink.delete()

        return jsonify({
          'success': True,
          'delete': drink.id
        })

      except:
        abort(422)
    else:
      abort(401)


  ## Error Handling
  '''
  Example error handling for unprocessable entity
  '''
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": "unprocessable"
                      }), 422

  '''
  @TODO implement error handlers using the @app.errorhandler(error) decorator
      each error handler should return (with approprate messages):
              jsonify({
                      "success": False, 
                      "error": 404,
                      "message": "resource not found"
                      }), 404

  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad request"
      }), 400
  '''
  @TODO implement error handler for 404
      error handler should conform to general task above 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
      }), 404

  '''
  @TODO implement error handler for AuthError
      error handler should conform to general task above 
  '''
  @app.errorhandler(AuthError)
  def authorization_error(error):
    return jsonify({
      "success": False,
      "error": error.status_code,
      "message": error.error['description']
      }), 401

  @app.errorhandler(403)
  def not_found_permission(error):
    return jsonify({
      "success": False, 
      "error": 403,
      "message": "Do not have permissions"
      }), 403

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Server error"
      }), 500

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)