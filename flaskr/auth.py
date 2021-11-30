import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import re
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        re_enter_password = request.form['re-enter-password']
        emailRegex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif re.fullmatch(emailRegex, email) is None:
            error = 'Invalid Email. Please try a valid email'
        elif not password:
            error = 'Password is required.'
        elif password != re_enter_password:
            error = 'Password not match.'

        if error is None:
            try:
                db.query_db(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.get_db().commit()
            except Exception as e:
                error = str(e)
            else:
                flash("Register successfully", category='success')
                return redirect(url_for("auth.login"))

        flash(error, category='error')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = db.query_db(
            "SELECT * FROM users WHERE email = :email",
            {"email": email},
            one=True
        )

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash("Login successfully", category='success')
            return redirect(url_for('store.store'))

        flash(error, category='error')

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.query_db(
            'SELECT * FROM users WHERE id = :user_id',
            {"user_id": user_id},
            one=True
        )
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('store.store'))

# Check user login for other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view