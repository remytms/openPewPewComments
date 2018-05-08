# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <14291@student.ecam.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""
DB manager for openPewPewComments
"""


import sqlite3


INIT_BDFILE = "db.sql"
GET_FIELD = ['id', 'post', 'user', 'content', 'datetime_int']


class CommentsManager:
    """Little ORM for comments"""

    def __init__(self, dbfile='comments.db'):
        try:
            db = sqlite3.connect(dbfile)
            curs = db.cursor()
            with open(INIT_BDFILE, 'r') as init_db_file:
                init_db_query = init_db_file.read()
            curs.execute(init_db_query)
            db.commit()
        except sqlite3.Error as err:
            print(err)
        except IOError as err:
            print(err)
        self._dbfile = dbfile
        self._table = 'comments'

    def write(self, cid=None, post=None, user=None, content="",
              datetime=0):
        db = sqlite3.connect(self._dbfile)
        curs = db.cursor()
        if post is not None and user is not None:
            if cid is None:
                sql = (
                    "INSERT INTO %s(post, user, content, datetime_int) "
                    "VALUES (?, ?, ?, ?)"
                    % (self._table)
                )
            else:
                sql = (
                    "UPDATE %s SET "
                    "post = ?, "
                    "user = ?, "
                    "content = ?, "
                    "datetime_int = ? "
                    "WHERE id = ?"
                    % (self._table)
                )
            try:
                if cid is None:
                    curs.execute(sql, (post, user, content, datetime))
                else:
                    curs.execute(sql, (post, user, content, datetime, cid))
                db.commit()
            except sqlite3.Error as err:
                print(err)
                return False
            finally:
                db.close()
            return True
        return False

    def search(self, post=None, user=None):
        """Search comments in db"""
        db = sqlite3.connect(self._dbfile)
        curs = db.cursor()
        sql = (
            "SELECT id, post, user, content, datetime_int "
            "FROM %s "
            % (self._table)
        )
        try:
            if post and user:
                curs.execute(sql+"WHERE post = ? AND user = ?", post, user)
            elif post:
                curs.execute(sql+"WHERE post = ?", post)
            elif user:
                curs.execute(sql+"WHERE user = ?", user)
            else:
                curs.execute(sql)
            res = curs.fetchall()
            db.commit()
        except sqlite3.Error as err:
            print(err)
            return False
        finally:
            db.close()
        return res

    def get(self, cid):
        """Get the comment corresponding to the ID"""
        db = sqlite3.connect(self._dbfile)
        curs = db.cursor()
        sql = (
            "SELECT id, post, user, content, datetime_int "
            "FROM %s "
            % (self._table)
        )
        try:
            sql += "WHERE id is 2;"
            curs.execute(sql)
            db.commit()
            res = curs.fetchall()
        except sqlite3.Error as err:
            print(err)
            return False
        finally:
            db.close()
        return res

    def delete(self, cid):
        """Delete the comments corresponding to the given ID"""
        db = sqlite3.connect(self._dbfile)
        curs = db.cursor()
        sql = "DELETE FROM %s WHERE id = ?" % (self._table)
        try:
            curs.execute(sql, (cid, ))
            db.commit()
        except sqlite3.Error as err:
            print(err)
            return False
        finally:
            db.close()
        return True

