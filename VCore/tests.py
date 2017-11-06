#!/bin/env python3
# -*- encoding: utf-8 -*-

import os
import sys,random

from flask import current_app as app, render_template, request, jsonify, session, Blueprint, render_template_string
from . import plugins
from .models import db,Webshell

tests = Blueprint('tests', __name__)

def randomstr():
    res = ""
    s = "qwertyuiopasdfghjklzxcvbnm,.1234567890-=!@#$%^&*()_ZXCVBNM<>?ASDFGHJKL:WERTYIOP"
    for i in range(0,128):
        res =res+ random.choice(s)
    return res

@tests.route("/test", methods=['GET'])
def test():
    _types = ['php', 'asp', 'aspx', 'jsp']
    for t in _types:
        for i in range(0,25):
            db.session.add(Webshell(t, random.choice([1, 0]), randomstr()))
            db.session.commit()
    db.session.close()
    return render_template_string('ok')


@tests.route("/webshells", defaults={'shell_type': '', 'page': '1'}, methods=['GET'])
@tests.route("/webshells/<shell_type>", defaults={'page': '1'}, methods=['GET'])
@tests.route("/webshells/<shell_type>/<int:page>", methods=['GET'])
def tests_webshells(shell_type="", page=1):
    _types = ['php', 'asp', 'aspx', 'jsp']
    page = abs(int(page))
    results_per_page = 10
    page_start = results_per_page * (page - 1)
    page_end = results_per_page * (page - 1) + results_per_page
    webshells = []
    pages = 0
    if shell_type in _types:
        count = Webshell.query.filter_by(type=shell_type).count()
        print(count)
        webshells = Webshell.query.filter_by(
            type=shell_type).slice(page_start, page_end).all()
        print(webshells)
        pages = int(count / results_per_page) + (count % results_per_page > 0)
        print(pages)
    else:
        # prit
        pass
    return render_template("webshells.html", webshells=webshells, type=shell_type, pages=pages, curr_page=page)


@tests.route("/webshell/<int:id>", methods=['GET'])
def tests_webshell(id=0):
    if id:
        webshell = Webshell.query.filter_by(id=id).first()
        return jsonify(status=1, data=webshell)
    return jsonify(status=0)


@tests.route("/cryptos", methods=['GET'])
def tests_cryptos():
    cryptos = plugins.crypto.__all__
    print(cryptos)
    return render_template("cryptos.html", cryptos=cryptos)


@tests.route("/crypto/<int:id>", methods=['GET'])
def tests_crypto(id=0):
    return jsonify(status=0)
