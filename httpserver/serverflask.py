#!/usr/bin/env python

from flask import Flask, request
import pastebinlib.db_kyoto as dbk
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome to plumbum."

@app.route('/<uid>', methods=['GET'])
def show_entry(uid):
    print uid
    try:
        code = dbk.retrieve(uid)
    except dbk.DataBaseError:
        return "Error uid: %s not found." % uid
    else:
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(full=True, style='colorful')
        return highlight(code, lexer, formatter)

@app.route('/', methods=['POST'])
def add_entry():
    code = request.form["lead"]
    uid = dbk.post(code)
    return "http://127.0.0.1:5000/%s\n" % uid

if __name__ == "__main__":
    dbk.init()
    app.run()
    dbk.bye()
