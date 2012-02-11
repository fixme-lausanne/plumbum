from bottle import run, route, request

@route('/', method='POST')
def index():
    return ""
def start():
    run(host='localhost', port=8080)
    
start()
