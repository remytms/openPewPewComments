# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <14291@student.ecam.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
REST API for openPewPewComments
"""


from flask_classy import FlaskView, route, make_response, request
from flask.json import jsonify

from db import CommentsManager, GET_FIELD


class CommentsView(FlaskView):
    """API for comments"""

    def index(self):
        return self.get(None)

    def get(self, comment_id):
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

    def post(self):
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

    def delete(self, comment_id):
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

    def put(self, comment_id):
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
