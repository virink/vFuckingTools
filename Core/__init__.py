#!/usr/bin/env python3

import sys
import os

from flask import Flask, render_template, request, redirect, jsonify, json as json_mod, url_for, Response
from flask_session import Session

from Core.models import db
from Core.utils import init_utils
from Core.views import views
from Core.admin import admin


def create_app(config='Core.config.devConfig'):
    app = Flask("Core")
    with app.app_context():
        app.config.from_object(config)
        Session(app)
        db.init_app(app)
        db.create_all()
        app.db = db
        init_utils(app)
        app.register_blueprint(views)
        app.register_blueprint(admin)
    return app
