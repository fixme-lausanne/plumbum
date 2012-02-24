#!/usr/bin/env python3
"""plumbum http server based on bottle"""
from os.path import dirname, abspath, join
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import logging
try:
    from pygments import highlight
    from pygments.lexers import guess_lexer
    from pygments.formatters import HtmlFormatter
    PYGMENT_SET = True
except ImportError:
    logging.error('Cannot import pygments lib, will not provide \
coloration')
    PYGMENT_SET = False
    
import database as db
from bottle import run, request, abort, HTTPResponse, Bottle
from bottle import template as _template

RAW_USER_AGENT = ["curl", "wget", "links", "lynks", "elinks"]

def template(path, base='templates', **kwargs):
    """Generate the content of the template"""
    return _template(join(base, path), kwargs)

plumbum = Bottle()


@plumbum.route('/', method='GET')
def index():
    """Display the home page"""
    return template('paste_form')


@plumbum.route('/', method='POST')
def post():
    """Post a new pastebin"""
    content = request.forms.get('content')
    if content == "":
        abort(404, "You must provide a content")
    prefered_uid = request.forms.get('puid')
    if not prefered_uid:
        prefered_uid = None
    uid = db.post(content, prefered_uid=prefered_uid)
    url = '%s%s' % (request.url, uid)
    raw_url = url + '/raw'
    if request.forms.get('from_form'):
        return template('paste_done', url=url, raw_url=raw_url)
    else:
        return HTTPResponse(raw_url, status=201, header={'Location': raw_url})


@plumbum.route('/:uid/raw', method='GET')
@plumbum.route('/:uid/raw/', method='GET')
def raw_retrieve(uid):
    """Fetch a pastebin entry without coloration"""
    try:
        return db.retrieve(uid)
    except db.NonExistentUID:
        abort(404, 'No such item "%s"' % uid)


@plumbum.route('/:uid', method='GET')
@plumbum.route('/:uid/', method='GET')
def retrieve(uid):
    """Fetch a pastebin entry with coloration using Pygments lib"""
    user = request.get_header("User-Agent")
    if not user or user.split("/")[0] in RAW_USER_AGENT:
        return raw_retrieve(uid)
    if PYGMENT_SET :
        try:
            raw_paste = db.retrieve(uid)
            colorized_style = HtmlFormatter().get_style_defs('.highlight')
            colorized_content = highlight(raw_paste, guess_lexer(raw_paste),
             HtmlFormatter())
            return template('colorized', uid=uid, 
            colorized_style=colorized_style, 
            colorized_content=colorized_content)
        except db.NonExistentUID:
            logging.debug("404 occured on item %s" % uid)
            abort(404, 'No such item "%s"' % uid)
    else:
        return raw_retrieve(uid)

def start(host='0.0.0.0', port=8080, wsgi=False, server=):
    """start the app, that's all"""
    logging.debug("Launching the bottleServer")
    run(app=plumbum, host=host, port=port)

def _start_as_wsgi():
    
if __name__ == '__main__':
    """Start the server if it's launch directly from the command line. 
    It will be in DEBUG mode
    """
    logging.getLogger().setLevel(logging.DEBUG)
    run(plumbum, host='localhost', port=8080, debug=True, reloader=True)
