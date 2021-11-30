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

