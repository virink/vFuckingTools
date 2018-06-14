#!/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import os
import imp

from flask import Flask, render_template, request, redirect, jsonify, json as json_mod, url_for, Response
# from flask_session import Session

from models import db
from utils import init_utils
from auths import auths
from views import views
from tests import tests
import plugins


def create_app(config='config.devConfig'):
    app = Flask("vFuckingTools")
    with app.app_context():
        app.config.from_object(config)
        # Session(app)
        db.init_app(app)
        db.create_all()
        app.db = db
        init_utils(app)
        app.register_blueprint(auths)
        app.register_blueprint(views)
        app.register_blueprint(tests)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8181)
