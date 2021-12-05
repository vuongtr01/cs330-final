from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from . import db

bp = Blueprint('store', __name__)

@bp.route('/')
@login_required
def store():
    books = db.query_db("Select * from books limit 20")
    return render_template('store/store.html', books = books)

@bp.route('/item/<int:item_id>')
@login_required
def item_details(item_id):
    item = db.query_db(
        "Select * from books Where id=:item_id",
        {"item_id": item_id},
        one=True
        )
    return render_template('store/item.html', item = item)

@bp.route('/item/orders')
@login_required
def orders():
    return render_template('store/orders.html')

@bp.route('/checkout')
@login_required
def checkout():
    return render_template('store/cart.html')