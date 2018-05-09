# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <14291@student.ecam.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
Authentication process for openPewPewComments
"""


from flask import request
from flask.json import jsonify
from functools import wraps

import jwt


SECRET = 'secret'


def auth_required(func):
    @wraps(func)
    def decorated(*args, **kw):
        try:
            token = request.headers['x-access-token']
        except KeyError:
            return jsonify(
                {'error': "No auth possible: Token is missing"}
            ), 401

        try:
            token_data = jwt.decode(token, SECRET)
            user = token_data['user']
        except:
            return jsonify(
                {'error': "No auth possible: Token is invalid"}
            ), 401

        return func(user, *args, **kw)
    return decorated
