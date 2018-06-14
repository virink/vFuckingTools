#!/bin/env python3
# -*- encoding: utf-8 -*-

import os

##### GENERATE SECRET KEY #####
with open('.vtoolkit_secret_key', 'ab+') as secret:
    secret.seek(0)
    key = secret.read()
    if not key:
        key = os.urandom(64)
        secret.write(key)
        secret.flush()
##### SERVER SETTINGS #####


class Config(object):
    AUTH = 'Virink'
    SECRET_KEY = os.environ.get('SECRET_KEY') or key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_NAME = "session"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "/tmp/flask_session"
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 604800  # 7 days in seconds
    TEMPLATES_AUTO_RELOAD = True
    SITESEO = {
        'title': 'CTFTools',
        'description': 'The Tools for CTF&AWD by GinkgoTeam',
        'keyword': 'Security,CTF,AWD'
    }


class devConfig(Config):

    def __init__(self):
        self.DEBUG = True
