from bottle import route, run, request, default_app
import pastebinlib.db_kyoto as dbk
from pastebinlib.api import NonExistentUID

@route('/<uid>', method='GET')
def retrieve(uid=None):
    if not uid:
        return "Nope"
    try:
        content = dbk.retrieve(uid)
    except NonExistentUID:
        return "Nope"
    return content
    
@route('/', method='POST')
def post(prefered_uid=None):
    content = request.forms.get('lead')
    uid = dbk.post(content, prefered_uid=prefered_uid)
    return uid
    
def run_this_crap(port=8080, host='localhost'):
    dbk.init()
    run(host=host, port=port)
