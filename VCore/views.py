#!/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys
import time

from flask import current_app as app, render_template, request, jsonify, session, Blueprint, render_template_string

# import VCore.plugins
# try:
from . import plugins
# except:
# from VCore import plugins

views = Blueprint('views', __name__)


@views.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@views.route("/test", methods=['GET'])
def test():
    res = plugins.libs.ds_store.func_ds_store(
        "http://www.audit.virzz.com/.DS_Store")
    return render_template_string(','.join(res))
