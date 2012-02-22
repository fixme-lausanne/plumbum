#!/usr/bin/env python3

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
import logging
import socket
from threading import Semaphore, Thread
from time import sleep
import logging

# Add the parent path of this file to pythonpath, so we can import database
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import database as db

class GeneralHandler(SocketServer.BaseRequestHandler):
    BUF_SIZE = 1024
    def setup(self):
        logging.debug(self.client_address, 'connected!')
        
    def finish(self):
        logging.debug(self.client_address, 'disconnected')
        
class GetHandler(GeneralHandler):
    def handle(self):
        """handle the retrieving of a already created pastebin from
        a existant connexion, then close the connexion"""
        #handle the get request
        uid = list()
        while 1:
            buf = self.request.recv(GeneralHandler.BUF_SIZE).decode("UTF-8")
            logging.debug("Uid buffer is :|%s|" % buf)
            #if buf == b'\xff\xec':
                #telnet support
            #    break
            if '\x0a' in buf:
                #netcat support
                uid += buf
                break
            uid += buf
        decoded_uid = "".join(uid).rstrip()
        logging.debug("Uid decoded is |%s|" % decoded_uid)
        try:
            data = db.retrieve(decoded_uid)
        except db.NonExistentUID:
            data = "Uid %s not found" % decoded_uid
        state = self.request.sendall(data.encode("UTF-8"))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')
        logging.debug('Data retrieved')

class PostHandler(GeneralHandler):
    
    def handle(self):
        """handle the depot of a new paste from an already alive
        connexion"""
        #handle the post request
        content = list()
        while 1:
            buf = self.request.recv(GeneralHandler.BUF_SIZE).decode("UTF-8")
            #if buf == b'\xff\xec':
            #    telnet support
            #    break
            if '\x0a' in buf:
                #netcat support
                content += buf
                break
            content += buf
        decoded_content = "".join(content).rstrip()
        logging.debug("Content uploaded is :|%s|".format(decoded_content))
        uid = db.post(decoded_content)
        logging.debug("content retrieved " + db.retrieve(uid))
        logging.debug("Uid is :|%s|" % uid)
        state = self.request.sendall((uid + "\r\n").encode('UTF-8'))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')

    #server host is a tuple ('host', port)

def start(host=''):
    post_server = SocketServer.ThreadingTCPServer((host, 1338), PostHandler)
    get_server = SocketServer.ThreadingTCPServer((host, 1339), GetHandler)
    post_server.serve_forever()
    get_server.serve_forever()

if __name__ == "__main__":
    sys.stderr.write("Debug mode \n")
    logging.getLogger().setLevel(logging.DEBUG)
    start()
