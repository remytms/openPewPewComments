# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <14291@student.ecam.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
REST API for openPewPewComments
"""


from flask_classy import FlaskView, route, make_response, request
from flask.json import jsonify

from auth import auth_required
from db import CommentsManager, GET_FIELD


class CommentsView(FlaskView):
    """API for comments"""

    @auth_required
    def index(self, user=None):
        return self.get()

    @auth_required
    def get(self, user=None, comment_id=None):
        com_mgr = CommentsManager()
        resp_dic = {'comments': []}
        if comment_id is None:
            comments = com_mgr.search()
        else:
            comments = com_mgr.get(comment_id)
        for comment in comments:
            comment_dic = {}
            for idx, field_name in enumerate(GET_FIELD):
                comment_dic.update({field_name: comment[idx]})
            resp_dic['comments'].append(comment_dic)
        return jsonify(resp_dic), 200

    @auth_required
    def post(self, user=None):
        com_mgr = CommentsManager()
        resp_dic = {'error': False}
        if not request.json:
            resp_dic['error'] = "No json given"
            return jsonify(resp_dic), 400
        if 'comment' not in request.json:
            resp_dic['error'] = "No field 'comment' in json"
            return jsonify(resp_dic), 400
        comment = request.json['comment']
        if not comment:
            resp_dic['error'] = "No comment given"
            return jsonify(resp_dic), 400
        res = com_mgr.write(
            post=comment['post'],
            user=comment['user'],
            content=comment['content'],
            datetime=comment['datetime_int'],
        )
        if not res:
            resp_dic['error'] = "Error when writing comment in db"
            return jsonify(resp_dic), 400
        return jsonify(resp_dic), 200

    @auth_required
    def delete(self, user=None, comment_id=None):
        com_mgr = CommentsManager()
        resp_dic = {'error': False}
        if comment_id is None:
            resp_dic['error'] = "No comment given"
            return jsonify(resp_dic), 400
        res = com_mgr.delete(comment_id)
        if not res:
            resp_dic['error'] = "Error when writing comment in db"
            return jsonify(resp_dic), 400
        return jsonify(resp_dic), 200

    @auth_required
    def put(self, user=None, comment_id=None):
        com_mgr = CommentsManager()
        resp_dic = {'error': False}
        if not request.json:
            resp_dic['error'] = "No json given"
            return jsonify(resp_dic), 400
        if 'comment' not in request.json:
            resp_dic['error'] = "No field 'comment' in json"
            return jsonify(resp_dic), 400
        comment = request.json['comment']
        if not comment:
            resp_dic['error'] = "No comment given"
            return jsonify(resp_dic), 400
        res = com_mgr.write(
            cid=comment_id,
            post=comment['post'],
            user=comment['user'],
            content=comment['content'],
            datetime=comment['datetime_int'],
        )
        if not res:
            resp_dic['error'] = "Error when writing comment in db"
            return jsonify(resp_dic), 400
        return jsonify(resp_dic), 200
