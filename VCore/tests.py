#!/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys

from flask import current_app as app, render_template, request, jsonify, session, Blueprint, render_template_string
from . import plugins

tests = Blueprint('tests', __name__)


@tests.route("/test", methods=['GET'])
def test():
    return render_template_string('test')
