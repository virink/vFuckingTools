#!/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import time

from flask import current_app as app, render_template, request, jsonify, session, Blueprint, render_template_string
from . import plugins

views = Blueprint('views', __name__)


@views.route("/", methods=['GET'])
def views_index():
    return render_template('index.html')


@views.route("/about", methods=['GET'])
def views_about():
    return render_template('index.html')
