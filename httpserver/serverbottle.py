from bottle import route, run, request, Bottle
import pastebinlib.db_kyoto as dbk
from pastebinlib.api import NonExistentUID

app = Bottle()
@app.route('/')
def index():
    return 'Welcome to our pastebin app'

@app.route('/<uid>')
def retrieve(uid=None):
    if not uid:
        return index()
    try:
        content = dbk.retrieve(uid)
    except NonExistentUID:
        return index()
    return content
    
@app.route('/', method='POST')
def post(prefered_uid=None):
    content = request.forms.get('code')
    uid = dbk.post(content, prefered_uid=prefered_uid)
    return uid
    
def run_server(port=8000):
    dbk.init()
    run(app, port=port)
