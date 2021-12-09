from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db
from flaskr.models import *

bp = Blueprint('api', __name__, url_prefix='/api')

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
def query_to_dict(query):
    result = []
    for r in query:
        result.append(row2dict(r))
    return result

@bp.route('/book/item/<int:item_id>', methods=["GET"])
def get_item(item_id):
    item = Book.query.filter_by(id=item_id).first()
    try:
        if item:
            return jsonify(row2dict(item)), 200
        else:
            raise Exception("No book found")
    except Exception as error: 
        return {"Error": "Bad Request." + str(error)}, 400

@bp.route('/book/checkout', methods=["POST"])
def checkout():
    data = request.get_json()
    try:  
        for book in data:
            b = Order(user_id=g.user.id, book_id=book["id"], order_time=book['time'])
            db.session.add(b)
            db.session.commit()
        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400
    
@bp.route('/book/orders', methods=["GET"])
def orders():
    try:
        data = db.session.query(
            Order.id, Order.order_time, Book.img_url, Book.title
        ).select_from(Order).join(Book).filter(Order.user_id==g.user.id).all()
        json_data = []
        
        for d in data:
            ob = {
                "id": d[0],
                "order_time": d[1],
                "img_url": d[2],
                "title": d[3]
            }
            json_data.append(ob)
        return jsonify(json_data), 200
    except Exception as error:
        print(error)
        return {"Error": "Bad Request." + str(error)}, 400
    
@bp.route('/book/orders/delete/<int:order_id>', methods=["DELETE"])
def delete_order(order_id):
    try:
        order = Order.query.filter_by(id=order_id).first()
        db.session.delete(order)
        db.session.commit()
        return "Success", 200
    except Exception as error:
        print(error)
        return {"Error": "Bad Request." + str(error)}, 400