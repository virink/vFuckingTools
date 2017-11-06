#!/usr/bin/env python3

import sys
import os

from flask import Flask, render_template, request, redirect, jsonify, json as json_mod, url_for, Response
# from flask_session import Session

from .models import db
from .utils import init_utils
from .views import views

from . import plugins


def create_app(config='VCore.config.devConfig'):
    app = Flask("VCore")
    with app.app_context():
        app.config.from_object(config)
        # Session(app)
        db.init_app(app)
        db.create_all()
        app.db = db
        init_utils(app)
        app.register_blueprint(views)
    return app
