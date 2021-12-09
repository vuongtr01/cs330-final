from . import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String, unique=True)
    email = db.Column('email', db.String, unique=True)
    password = db.Column('password', db.String)
    orders = db.relationship("Order")
    
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    author = db.Column('author', db.String)
    publication_year = db.Column('publication_year', db.Integer)
    publisher = db.Column('publisher', db.String)
    img_url = db.Column('img_url', db.String)
    orders = db.relationship("Order")
    
class Order(db.Model):
    __tablename__ = 'order_history'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
    order_time = db.Column('order_time', db.Integer)
