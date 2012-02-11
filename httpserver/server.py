#!/usr/bin/env python

import logging
import re

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        header = open('templates/header.tpl', 'r').read()
        footer = open('templates/footer.tpl', 'r').read()
        length = int(self.headers.get('content-length'))
        post = self.rfile.read(length)
        logging.debug('post this to the db %s'%post)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(header+"Data received"+footer, 'utf-8'))

    def do_GET(self):
        reg = re.compile('[/]u[/]([a-zA-Z0-9]+)')
        header = open('templates/header.tpl', 'r').read()
        footer = open('templates/footer.tpl', 'r').read()
        m = reg.match(self.path)
        # Show paste
        if m != None:
            paste = 'Stuff from the database'
            data = open('templates/show.tpl', 'r').read().replace('{{data}}', paste)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(header+data+footer, 'utf-8'))
            return
        # Add paste
        else:
            data   = open('templates/form.tpl', 'r').read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(header+data+footer, 'utf-8'))
        

httpd = HTTPServer(('', 8000), RequestHandler)
httpd.serve_forever()

