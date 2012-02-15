#!/usr/bin/env python3
"""simple socket server with emulation of post/get using two port"""
import socket
from threading import Semaphore, Thread
from time import sleep
import logging

# Add the parent path of this file to pythonpath, so we can import database
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import database as db

class SocketServerManager(Thread):
    """Class that create the socket servers and assign callback to them"""

    """Size of the receive buffer"""
    BUF_SIZE = 1024

    def __init__(self, post_port=1338, get_port=1339, host='localhost'):
        """simple init, the server will be bound on host"""
        Thread.__init__(self)
        self.post_port = post_port
        self.get_port = get_port
        self.host = host
        self.servers = []
        post_serv = self.socket_server_factory(self.host, self.post_port,
self.post_handler)
        self.servers.append(post_serv)
        get_serv = self.socket_server_factory(self.host, self.get_port,
self.get_handler)
        self.servers.append(get_serv)

    def post_handler(self, conn, addr):
        """handle the depot of a new paste from an already alive
        connexion"""
        #handle the post request
        content = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE).decode("UTF-8")
            #if buf == b'\xff\xec':
                #telnet support
            #    break
            if '\x0a' in buf:
                #netcat support
                content += buf
                break
            content += buf
        decoded_content = "".join(content).rstrip()
        logging.debug("Content uploaded is :|{}|".format(decoded_content))
        uid = db.post(decoded_content)
        logging.debug("content retrieved " + db.retrieve(uid))
        logging.debug("Uid is :|{}|".format(uid))
        state = conn.sendall((uid + "\r\n").encode('UTF-8'))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')

    def get_handler(self, conn, addr):
        """handle the retrieving of a already created pastebin from
        a existant connexion, then close the connexion"""
        #handle the get request
        uid = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE).decode("UTF-8")
            logging.debug("Uid buffer is :|{}|".format(buf))
            #if buf == b'\xff\xec':
                #telnet support
            #    break
            if '\x0a' in buf:
                #netcat support
                uid += buf
                break
            uid += buf
        decoded_uid = "".join(uid).rstrip()
        logging.debug("Uid decoded is |{}|".format(decoded_uid))
        try:
            data = db.retrieve(decoded_uid)
        except db.NonExistentUID:
            data = "Uid {} not found".format(decoded_uid)
        state = conn.sendall(data.encode("UTF-8"))
        if state:
            logging.debug('Data not fully transmitted')
            logging.warning('The data sent have not been transmitted properly')
        logging.debug('Data retrieved')

    def socket_server_factory(self, host, port, callback):
        """create a new SocketServer instance bound on the port port and
        host host. It will call the callback on new incoming connexion"""
        s = socket.getaddrinfo(host, port)
        server = SocketServer(callback, s)
        server.daemon = True
        return server

    def run(self):
        """start the servers and wait for them to be stopped"""
        try:
            for s in self.servers:
                s.start()
            for s in self.servers:
                s.join()
        except KeyboardInterrupt:
            for s in self.servers:
                s.close()
                
class SocketServer(Thread):
    """A simple telnet server with a callback"""

    """define the number of simultaneous thread that can be awaken to
    handle the connexions"""
    SEM_MAX = 30
    
    def __init__(self, callback_method, skts):
        """Simple init"""
        Thread.__init__(self)
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
            if msg.errno == socket.errno.EADDRINUSE:
                logging.error("Adress already in use, trying again in 30 seconds")
                sleep(30)
                s.close()
                self.bound(s)
                return
            elif msg.errno == socket.errno.ENOTSUP:
                logging.error("Cannot bind on this interface, as it is not enable")
                s.close()
                return
            else:
                logging.debug("Error while binding the socket : {}".format(str(msg)))
                logging.error("Could not start server, socket cannot be bound")
                return
        logging.debug("correctly bound on ")
        while 1:
            logging.info("Connexion done")
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
        #just to be sure that if anything goes really wrong during the 
        #connexion that the connection will be correctly closed
        try:
            fs(arg[0], arg[1])
        except Exception as e:
            logging.error(e)
        finally:
            arg[0].close()
            self.sem.release()
    
    def close(self):
        pass
        
def start():
    SocketServerManager().start()
    
if __name__ == "__main__":
    sys.stderr.write("Debug mode \n")
    logging.getLogger().setLevel(logging.DEBUG)
    SocketServerManager().run()
