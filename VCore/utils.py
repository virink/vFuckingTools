from flask import current_app as app, g, request, session, render_template, abort, redirect, url_for, jsonify
from sqlalchemy import create_engine
from functools import wraps
import time
import datetime
import hashlib
import os


def init_utils(app):
    app.jinja_env.filters['long2ip'] = long2ip
    app.jinja_env.globals.update(authed=authed)

    @app.context_processor
    def inject_user():
        if session:
            return dict(session)
        return dict()


def authed():
    return bool(session.get('auth', False))


def ip2long(ip):
    return unpack('!i', inet_aton(ip))[0]


def long2ip(ip_int):
    try:
        return inet_ntoa(pack('!i', ip_int))
    except struct_error:
        return inet_ntoa(pack('!I', ip_int))


def get_ip():
    return request.remote_addr


def sha512(string):
    return str(hashlib.sha512(string).hexdigest())
