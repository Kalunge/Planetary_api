from app import db, ma
from sqlalchemy import String, Float, Column, Integer, Numeric


class Planet(db.Model):
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    home_star = Column(String)
    distance = Column(Float)
    radius = Column(Float)
    mass = Column(Float)

class PlanetsSchema(ma.Schema):
    class Meta():
        fields = ('planet_id', 'planet_name', 'home_star', 'distance', 'radius', 'mass')

planet_schema = PlanetsSchema()
planets_schema = PlanetsSchema(many=True)