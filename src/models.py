from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(120), unique=True, nullable=False)
    password = Column(db.String(80), unique=False, nullable=False)
    is_active = Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # do not serialize the password, its a security breach
        }

    def __repr__(self):
        return '<User %r>' % self.username

class Favorites(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(250), nullable=False)
    user_id = Column(db.Integer, ForeignKey('user.id'))
    characters_id = Column(db.Integer, ForeignKey('characters.id'))
    planets_id = Column(db.Integer, ForeignKey('planets.id'))
    user = relationship(User)

class Characters(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    favorites = relationship(Favorites)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Planets(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    favorites = relationship(Favorites)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
