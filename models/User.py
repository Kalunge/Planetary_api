from app import db, ma
from sqlalchemy import String, Float, Column, Integer, Numeric



class User(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class UsersSchema(ma.Schema):
    class Meta():
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)