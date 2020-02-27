from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


from models.Planet import Planet, PlanetsSchema, planet_schema, planets_schema
from models.User import User, UsersSchema, users_schema, user_schema


@app.cli.command('db_create')
def create_db():
    db.create_all()
    print('Database Created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped')

    
@app.cli.command('db_seed')
def db_seed():
    Mercury = Planet(planet_name = 'Mercury',
    home_star = 'Sun',
    distance = 2145632.56589,
    radius = 215322.56685,
    mass = 2564522.4586)

    Venus = Planet(planet_name = 'Venus',
    home_star = 'Sundowner',
    distance = 2145632.56589,
    radius = 215322.56685,
    mass = 2564522.4586)


    Earth = Planet(planet_name = 'Earth',
    home_star = 'Sunser',
    distance = 4232323.56589,
    radius = 659856.56685,
    mass = 659856.4586)

    test_user = User(first_name = 'Titus',
    last_name = 'Muthomi',
    email = 'test@test.com',
    password = 'Passw0rd')

    db.session.add(Mercury)
    db.session.add(Venus)
    db.session.add(Earth)
    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')

@app.route('/', methods = ['GET'])
def index():
    planet_list = Planet.query.all()
    result = planets_schema.dump(planet_list)
    return jsonify(result)

@app.route('/users', methods = ['GET'])
def users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)

@app.route('/register', methods = ['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message = 'That user already exist'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']

        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message = 'User created succefully'), 201
        

    


    