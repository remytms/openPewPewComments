# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <14291@student.ecam.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
Server that run's openPewPewComments API
"""


from flask import Flask, request
from flask_cors import CORS

from comments import CommentsView


import sqlite3

app = Flask(__name__)
message = ""


# Custom routes
@app.route('/')
def hello():
    """Test method"""
    return 'Hello, World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Sniffable login page"""
    if request.method == 'GET':
        html = '<html>'
        html += '<head></head>'
        html += '<body>'
        html += '<form action="/login" method="POST">'
        html += '<label>Login: </label><input name="login" type="text"/><br/>'
        html += '<label>Password: </label><input name="pwd" type="password"/>'
        html += '<input type="submit" value="Submit">'
        html += '</form>'
        html += '</body>'
        html += '</html>'
    if request.method == 'POST':
        user = request.form['login']
        password = request.form['pwd']
        print(user, password)
        if user == 'mieg' and password == 'test':
            html = 'Logged'
        else:
            html = 'Wrong user or password'
    return html


@app.route('/post', methods=['GET', 'POST'])
def post_message():
    global message
    if request.method == 'POST':
        message = request.form['message']
    html = '<html>'
    html += '<head></head>'
    html += '<body>'
    html += '<form action="/post" method="POST">'
    html += '<label>Message: </label>'
    html += '<textarea name="message">'
    html += message
    html += '</textarea><br/>'
    html += '<input type="submit" value="Submit">'
    html += '</form>'
    html += '<p>Your message is :</p>'
    html += message
    html += '</body>'
    html += '</html>'
    return html


@app.route('/sql', methods=['GET', 'POST'])
def inject_sql():
    # Connect to a test db
    try:
        db = sqlite3.connect('test.db')
        curs = db.cursor()
        with open('db.sql', 'r') as init_db_file:
            init_db_query = init_db_file.read()
        curs.execute(init_db_query)
        db.commit()
    except sqlite3.Error as err:
        print(err)
    except IOError as err:
        print(err)
    if request.method == 'POST':
        message = request.form['message']
        # SQL request in a bad way
        sql = (
            "INSERT INTO %s(post, user, datetime_int, content) "
            "VALUES (1, 1, 1000, '%s');"
            % ('comments', message)
        )
        print(sql)
        curs.executescript(sql)
        db.commit()
    html = '<html>'
    html += '<head></head>'
    html += '<body>'
    html += '<form action="/sql" method="POST">'
    html += '<label>Message: </label>'
    html += '<textarea name="message">'
    html += '</textarea><br/>'
    html += '<input type="submit" value="Submit">'
    html += '</form>'
    html += '</body>'
    html += '</html>'
    db.close()
    return html


# Register views
CommentsView.register(app)


if __name__ == "__main__":
    app.run(port=8080)
    CORS(app)
