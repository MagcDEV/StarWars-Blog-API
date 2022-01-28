import os
import json
import requests
import math
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Characters, Planets

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)

with app.app_context():
    # Carga planetas a la BD
    print("Data Cargada")
    if len(Characters.query.all()) < 1:
        planets = requests.get('https://swapi.dev/api/planets').json()

        next_url = planets['next']
        while next_url != None:
            new_page = requests.get(next_url).json()
            planets['results'] += new_page['results']
            next_url = new_page['next']

        for x in planets['results']:
            planetas = Planets()
            planetas.name = x['name']
            db.session.add(planetas)
            db.session.commit()
            
        all_planets = Planets.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        #print(all_planets)

        # Carga personajes a la BD
        people = requests.get('https://swapi.dev/api/people').json()

        next_url = people['next']
        while next_url != None:
            new_page = requests.get(next_url).json()
            people['results'] += new_page['results']
            next_url = new_page['next']

        for x in people['results']:
            gente = Characters()
            gente.name = x['name']
            db.session.add(gente)
            db.session.commit()
            
        all_people = Characters.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        #print(all_people)

    """
    # Carga planetas a la BD

    planets = requests.get('https://swapi.dev/api/planets').json()

    if planets['next'] != None:
        next_url = planets['next']
        for x in range(math.trunc(planets["count"] / 10) - 1 ):
            if next_url != None:
                new_page = requests.get(next_url).json()
                planets['results'] += new_page['results']
                next_url = new_page['next']

    for x in planets['results']:
        planetas = Planets()
        planetas.name = x['name']
        db.session.add(planetas)
        db.session.commit()
        
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    print(all_planets)

    # Carga personajes a la BD
    people = requests.get('https://swapi.dev/api/people').json()

    if people['next'] != None:
        next_url = people['next']
        for x in range(math.trunc(people["count"] / 10) - 1 ):
            if next_url != None:
                new_page = requests.get(next_url).json()
                people['results'] += new_page['results']
                next_url = new_page['next']

    for x in people['results']:
        gente = Characters()
        gente.name = x['name']
        db.session.add(gente)
        db.session.commit()
        
    all_people = Characters.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    print(all_people)
    """

    """
    Characters.query.delete()
    db.session.commit()
    """


