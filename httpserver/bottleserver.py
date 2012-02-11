#!/usr/bin/env python3
"""Plumbum http server based on bottle"""
# Add the parent path of this file to pythonpath, so we can import pastebinlib
from os.path import dirname, abspath
import sys
import logging
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    logging.error('Cannot import pygments lib, will not provide \
coloration')
    
sys.path.append(dirname(dirname(abspath(__file__))))
from pastebinlib.api import NonExistentUID
try:
    import pastebinlib.db_kyoto as db
except ImportError:
    logging.error('Cannot import kyoto db, falling back to memory db \
(reason for failure: {})'.format(sys.exc_info()[0]))
    import pastebinlib.db_memory as db
from bottle import route, run, request, abort, template, HTTPResponse


@route('/', method='GET')
def index():
    """Display the home page"""
    return template('templates/paste_form')


@route('/', method='POST')
def post():
    """Post a new pastebin"""
    content = request.forms.get('content')
    #preferred_uid = request.forms.get('')
    uid = db.post(content)
    url = '%s%s' % (request.url, uid)
    if request.forms.get('from_form'):
        return template('templates/paste_done', url=url)
    else:
        return HTTPResponse(status=201, header={'Location': url})


@route('/:uid/raw', method='GET')
def raw_retrieve(uid):
    """Fetch a pastebin entry without coloration"""
    try:
        return db.retrieve(uid)
    except NonExistentUID:
        abort(404, 'No such item "%s"' % uid)


@route('/:uid', method='GET')
def retrieve(uid):
    """Fetch a pastebin entry with coloration using Pygments lib"""
    try:
        raw_paste = db.retrieve(uid)
        colorized_style = HtmlFormatter().get_style_defs('.highlight')
        colorized_content = highlight(raw_paste, PythonLexer(), HtmlFormatter())
        return template('templates/colorized', uid=uid, colorized_style=colorized_style, colorized_content=colorized_content)
    except NonExistentUID:
        abort(404, 'No such item "%s"' % uid)

if __name__ == '__main__':
    debug = True
    if debug:
        run(host='0.0.0.0', port=8080, debug=True, reloader=True)
    else:
        run(host='0.0.0.0', port=8080)
