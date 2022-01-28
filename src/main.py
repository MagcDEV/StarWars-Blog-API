"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
import math
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

import load_data


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people')
def getpeople():
    all_people = Characters.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/planets')
def getplanets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/users')
def getusers():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200

@app.route('/people/<int:person_id>')
def getonepeople(person_id):
    person = Characters.query.get(person_id)
    person = person.serialize()
    return jsonify(person), 200

@app.route('/planets/<int:planets_id>')
def getoneplanet(planets_id):
    planet = Planets.query.get(planets_id)
    planet = planet.serialize()
    return jsonify(planet), 200

@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def create_favorite_planet(planets_id):
    # POST request
    planeta = Planets.query.get(planets_id)
    favoritos = Favorites()
    favoritos.name = planeta.name
    favoritos.planets_id = planets_id
    favoritos.user_id = 1 # se asume el usuario actovo como el 1
    db.session.add(favoritos)
    db.session.commit()

    return "ok", 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_people(people_id):
    # POST request
    people = Characters.query.get(people_id)
    favoritos = Favorites()
    favoritos.name = people.name
    favoritos.characters_id = people_id
    favoritos.user_id = 1 # se asume el usuario actovo como el 1
    db.session.add(favoritos)
    db.session.commit()

    return "ok", 200

@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    # POST request
    planeta = Planets.query.get(planets_id)
    db.session.delete(planeta)
    db.session.commit()

    return "ok", 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # POST request
    person = Characters.query.get(people_id)
    db.session.delete(person)
    db.session.commit()

    return "ok", 200


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
