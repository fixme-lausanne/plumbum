#!/usr/bin/env python3

# Add the parent path of this file to pythonpath, so we can import pastebinlib
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

from bottle import route, run, request, abort, template, HTTPResponse
from pastebinlib.api import NonExistentUID
import pastebinlib.db_memory as db


@route('/', method='GET')
def index():
    return template('templates/paste_form')


@route('/', method='POST')
def post():
    content = request.forms.get('content')
    uid = db.post(content)
    url = '%s%s' % (request.url, uid)
    if request.forms.get('from_form'):
        return template('templates/paste_done', url=url)
    else:
        return HTTPResponse(status=201, header={'Location': url})


@route('/<uid>')
def retrieve(uid):
    try:
        return db.retrieve(uid)
    except NonExistentUID:
        abort(404, 'No such item "%s"' % uid)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
