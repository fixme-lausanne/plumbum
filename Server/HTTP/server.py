#!/usr/bin/env python

from http.server import *
from pprint import pprint
import re

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print('received POST: '+self.path)

    def do_GET(self):
        reg = re.compile('\/u\/([a-zA-Z0-9]+)')
        m = reg.match(self.path)
        if m != None:
            print('got id: %s'%m.group(1))

        print('received GET'+self.path)
        

httpd = HTTPServer(('', 8000), RequestHandler)
httpd.serve_forever()

