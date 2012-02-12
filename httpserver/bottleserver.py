#!/usr/bin/env python3
"""Plumbum http server based on bottle"""
from os.path import dirname, abspath, join
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import logging
try:
    from pygments import highlight
    from pygments.lexers import guess_lexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    logging.error('Cannot import pygments lib, will not provide \
coloration')
import database as db
from bottle import run, request, abort, HTTPResponse, Bottle
from bottle import template as _template

def template(path, base='templates', **kwargs):
    return _template(join(base, path), kwargs)

plubum = Bottle()

@plubum.route('/', method='GET')
def index():
    """Display the home page"""
    return template('paste_form')


@plubum.route('/', method='POST')
def post():
    """Post a new pastebin"""
    content = request.forms.get('content')
    #preferred_uid = request.forms.get('')
    uid = db.post(content)
    url = '%s%s' % (request.url, uid)
    if request.forms.get('from_form'):
        return template('paste_done', url=url)
    else:
        return HTTPResponse(status=201, header={'Location': url})


@plubum.route('/:uid/raw', method='GET')
@plubum.route('/:uid/raw/', method='GET')
def raw_retrieve(uid):
    """Fetch a pastebin entry without coloration"""
    try:
        return db.retrieve(uid)
    except db.NonExistentUID:
        abort(404, 'No such item "%s"' % uid)


@plubum.route('/:uid', method='GET')
@plubum.route('/:uid/', method='GET')
def retrieve(uid):
    """Fetch a pastebin entry with coloration using Pygments lib"""
    try:
        raw_paste = db.retrieve(uid)
        colorized_style = HtmlFormatter().get_style_defs('.highlight')
        colorized_content = highlight(raw_paste, guess_lexer(raw_paste), HtmlFormatter())
        return template('colorized', uid=uid, colorized_style=colorized_style, colorized_content=colorized_content)
    except db.NonExistentUID:
        abort(404, 'No such item "%s"' % uid)
    except NameError:
        return raw_retrieve(uid)

def start(host='0.0.0.0', port=8080):
    logging.debug("Launching the bottleServer")
    run(app=plubum, host=host, port=port)

if __name__ == '__main__':
    run(plubum, host='localhost', port=8080, debug=True, reloader=True)
