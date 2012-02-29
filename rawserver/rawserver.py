#!/usr/bin/env python3

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
import logging
import socket
from threading import Thread
from time import sleep
import logging

# Add the parent path of this file to pythonpath, so we can import database
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import api

class GeneralHandler(SocketServer.BaseRequestHandler):
    BUF_SIZE = 1024
    
    @staticmethod
    def set_v6():
        GeneralHandler.address_family = socket.AF_INET6
        
    def setup(self):
        logging.debug('%s connected!' % str(self.client_address))
        
    def finish(self):
        logging.debug('%s disconnected' % str(self.client_address))
        
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
            data = api.retrieve(decoded_uid)
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
            logging.debug("Uid buffer is :|%s|" % buf)
            #if buf == b'\xff\xec':
            #    telnet support
            #    break
            if '\x0a' in buf:
                #netcat support
                content += buf
                break
            content += buf
        decoded_content = "".join(content).rstrip()
        logging.debug("Content uploaded is :|%s|" % decoded_content)
        uid = api.post(decoded_content)
        logging.debug("Uid is :|%s|" % uid)
        state = self.request.sendall(uid.encode('UTF-8'))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')

def start(host=''):
    post_server = SocketServer.ThreadingTCPServer((host, 1338), PostHandler)
    get_server = SocketServer.ThreadingTCPServer((host, 1339), GetHandler)
    Thread(target=get_server.serve_forever).start()
    logging.debug("get is started !!")
    post_server.serve_forever()
    logging.debug("post is started !!")
    
if __name__ == "__main__":
    sys.stderr.write("Debug mode \n")
    logging.getLogger().setLevel(logging.DEBUG)
    start()
