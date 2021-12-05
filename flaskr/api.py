from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/book/item/<int:item_id>', methods=["GET"])
def get_item(item_id):
    item = db.query_db(
        "Select * from books Where id=:item_id",
        {"item_id": item_id},
        one=True
    )
    try:
        if item:
            return jsonify(item), 200
        else:
            raise Exception("No book found")
    except Exception as error: 
        return {"Error": "Bad Request." + str(error)}, 400

@bp.route('/book/checkout', methods=["POST"])
def checkout():
    data = request.get_json()
    try:  
        for book in data:
            db.query_db(
                "Insert Into order_history (user_id, book_id, order_time) VALUES(:user_id, :book_id, :order_time)",
                {"user_id": g.user["id"], "book_id": book["id"], "order_time": book["time"]}
            )
            db.get_db().commit()
        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400
    
@bp.route('/book/orders', methods=["GET"])
def orders():
    try:
        data = db.query_db(
            "Select order_history.id, order_history.order_time, books.img_url, books.title From order_history inner join books on order_history.book_id = books.id Where order_history.user_id=:user_id ",
            {"user_id": g.user["id"]}
        )
        return jsonify(data), 200
    except Exception as error:
        print(error)
        return {"Error": "Bad Request." + str(error)}, 400
    
@bp.route('/book/orders/delete/<int:order_id>', methods=["DELETE"])
def delete_order(order_id):
    try:
        db.query_db(
            "Delete From order_history Where id = :order_id ",
            {"order_id": order_id}
        )
        db.get_db().commit()
        return "Success", 200
    except Exception as error:
        print(error)
        return {"Error": "Bad Request." + str(error)}, 400