from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os
from flask_mail import Mail, Message


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-simple' 
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


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
        

@app.route('/login', methods = ['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='login successful', access_token=access_token)
    else:
        return jsonify(message='You entered a wrong password/email'), 401

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email:str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message('your planetary_api password is '+ user.password,
        sender='apip@planetary.com',
        recipients=[email])
        mail.send(msg)

        return jsonify(message=f'password was sent to {user.email}')
    else:
        return jsonify(message='that email doesnt exist'), 401


@app.route('/planet_details/<int:planet_id>')
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result), 200
    else:
        return jsonify(message='that planet does not exist'), 404



@app.route('/add_planet', methods=['POST'])
@jwt_required
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name = planet_name).first()

    if test:
        return jsonify(message='A planet with that name already exists'), 409
    else:
        home_star = request.form['home_star']
        distance = float(request.form['distance'])
        radius = float(request.form['radius'])
        mass = float(request.form['mass'])

        new_planet = Planet(planet_name=planet_name,
        home_star = home_star,
        distance = distance,
        radius = radius,
        mass = mass)

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(message='new planet added successfully'), 201


@app.route('/update_planet', methods=['PUT'])
@jwt_required
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.home_star = request.form['home_star']
        planet.distance = float(request.form['distance'])
        planet.radius = float(request.form['radius'])
        planet.mass = float(request.form['mass'])

        db.session.commit()
        return jsonify(message='You updated a planet'), 200
    else:
        return jsonify(message='That planet does not exist'), 404

@app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
@jwt_required
def remove_planet(planet_id : int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message='You deleted a planet successfully'), 202
    else:
        return jsonify(message='That planet doe not exist'), 404