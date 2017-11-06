#!/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import time

from flask import current_app as app, render_template, request, jsonify, session, Blueprint

views = Blueprint('views', __name__)


@views.route("/", methods=['GET'])
def index():
    return render_template('index.html')

