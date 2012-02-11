#!/usr/bin/env python3
"""simple socket server with emulation of post/get using two port"""
import socket
from multiprocessing import Process
from threading import Semaphore, Thread
import logging

# Add the parent path of this file to pythonpath, so we can import database
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

try:
    import database.db_kyoto as db
except:
    print('Cannot import kyoto db, falling back to memory db \
(reason for failure: %s)' % sys.exc_info()[0])
    import database.db_memory as db

from database.api import NonExistentUID


class SocketServerManager():
    """Class that create the socket servers and assign callback to them"""

    """Size of the receive buffer"""
    BUF_SIZE = 1024

    def __init__(self, post_port=1338, get_port=1339, host=None):
        """simple init, the server will be bound on host"""
        Process.__init__(self)
        self.post_port = post_port
        self.get_port = get_port
        self.host = host
        self.servers = []
        post_serv = self.socket_server_factory(self.host, self.post_port,
self.get_handler)
        self.servers.append(post_serv)
        get_serv = self.socket_server_factory(self.host, self.get_port,
self.post_handler)
        self.servers.append(get_serv)

    def post_handler(self, conn, addr):
        """handle the depot of a new paste from an already alive
        connexion"""
        #handle the post request
        content = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE)
            if buf == b'\xff\xec' or buf == b'\x0a':
                break
            content += buf
        uid = db.post("".join(map(str, content)))
        state = conn.sendall((uid + "\r\n").encode('UTF-8'))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')
        conn.close()

    def get_handler(self, conn, addr):
        """handle the retrieving of a already created pastebin from
        a existant connexion, then close the connexion"""
        #handle the get request
        uid = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE)
            if not buf:
                break
            uid += buf
        try:
            data = db.retrieve(uid)
        except NonExistentUID:
            data = "Uid %s not found" % uid
        state = conn.sendall(data.encode("UTF-8"))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')
        conn.close()
        print('Data retrieved')

    def socket_server_factory(self, host, port, callback):
        """create a new SocketServer instance bound on the port port and
        host host. It will call the callback on new incoming connexion"""
        s = socket.getaddrinfo(host, port)
        server = SocketServer(callback, s)
        server.daemon = True
        return server

    def run(self):
        """start the servers and wait for them to be stopped"""
        for s in self.servers:
            s.start()
        for s in self.servers:
            s.join()


class SocketServer(Process):
    """A simple telnet server with a callback"""

    """define the number of simultaneous thread that can be awaken to
    handle the connexions"""
    SEM_MAX = 30

    def __init__(self, callback_method, skts):
        """Simple init"""
        Process.__init__(self)
        self.callback = callback_method
        self.skts = skts
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def bound(self, s):
        """Bound the server to the socket and listen to new connection"""
        af, socktype, proto, _canonname, sa = s
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            return

        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            #pretty bad
            print(msg)
            s.close()
            s = None

        if s is None:
            logging.error("Could not start server, socket cannot be bound")
            return

        while 1:
            print("CONNECTION")
            acc = s.accept()
            t = Thread(target=self.with_sem, args=(self.callback, acc))
            t.run()

    def run(self):
        """run the server"""
        threads = []
        for skt in self.skts:
            thread = Thread(target=self.bound, args=(skt, ))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

    def with_sem(self, fs, arg):
        """Decorator for the callback function, limite the maximum
        number of simultaneous thread"""
        self.sem.acquire()
        fs(arg[0], arg[1])
        self.sem.release()

def start():
    SocketServerManager().run()

if __name__ == "__main__":
    SocketServerManager().run()
