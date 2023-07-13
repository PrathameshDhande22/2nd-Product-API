from mongoengine import *

""" MongoDB ORM models """


class Products(Document):
    name = StringField()
    uname = StringField()
    tags = StringField()
    seller = StringField()
    addedDate = DateField()
    price = FloatField()
    email = EmailField()


class User(Document):
    name = StringField()
    phoneno = IntField()
    email = EmailField()
    address = StringField()
    city = StringField()
    state = StringField()
    pincode = IntField()
    age = IntField()
    password = StringField()
    carts = ListField()
    history = ListField()
