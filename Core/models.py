#!/bin/env python3
# -*- encoding: utf-8 -*-

import datetime
import hashlib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError

db = SQLAlchemy()


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orz = db.Column(db.String(128))

    def __init__(self, orz):
        self.orz = orz

    def __repr__(self):
        return '<id %r>' % self.id

