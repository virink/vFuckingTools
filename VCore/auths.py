#!/bin/env python3
# -*- encoding: utf-8 -*-


from flask import current_app as app, render_template, request, jsonify, session, Blueprint
from . import plugins

auths = Blueprint('auths', __name__)


@auths.route("/login", methods=['GET'])
def auths_login():
    return render_template('index.html')


@auths.route("/logout", methods=['GET'])
def auths_logout():
    return render_template('index.html')


@auths.route("/register", methods=['GET'])
def auths_register():
    return render_template('index.html')
