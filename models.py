#!/bin/env python3
# -*- encoding: utf-8 -*-

import datetime
import hashlib

from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import DatabaseError

db = SQLAlchemy()


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orz = db.Column(db.String(128))

    def __init__(self, orz):
        self.orz = orz

    def __repr__(self):
        return '<id %r>' % self.id


class Webshell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    size = db.Column(db.Boolean, default=True)
    content = db.Column(db.Text)

    def __init__(self, type, size, content):
        self.type = type
        self.size = size
        self.content = content

    def __repr__(self):
        return '<id %r>' % self.id
