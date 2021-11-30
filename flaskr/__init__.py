from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from . import db
import os

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.path.join('flaskr', 'final.sqlite'),
        CSVFILE = os.path.join('flaskr', 'Books.csv'),
        SECRET_KEY="final_app",
    )

    # if test config is passed, update app to use that config object
    if test_config:
        app.config.update(test_config)

    # create data base by running command: flask init-db
    db.init_app(app)

    # Registering Blueprints
    from . import auth, store, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(store.bp)

    return app
