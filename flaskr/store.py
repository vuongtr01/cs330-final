from flask import (
    Blueprint, render_template
)
from flaskr.auth import login_required
from flaskr.models import *

bp = Blueprint('store', __name__)

@bp.route('/')
@login_required
def store():
    books = Book.query.limit(20).all()
    return render_template('store/store.html', books = books)

@bp.route('/item/<int:item_id>')
@login_required
def item_details(item_id):
    item = Book.query.filter_by(id=item_id).first()
    return render_template('store/item.html', item = item)

@bp.route('/item/orders')
@login_required
def orders():
    return render_template('store/orders.html')

@bp.route('/checkout')
@login_required
def checkout():
    return render_template('store/cart.html')