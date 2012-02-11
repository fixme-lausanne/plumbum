import socket
from multiprocessing import Process
from threading import Semaphore
import logging

class SocketServerManager(Process):
    BUF_SIZE = 1024
    
    def __init__(self, post_port=1338, get_port=1339, host=None):
        Process.__init__(self)
        self.servers = []
        post_serv = SocketServerManager.socket_server_factory(host, post_port, self.get_handler)
        self.servers.append(post_serv)
        get_serv = SocketServerManager.socket_server_factory(host, get_port, self.post_handler)
        self.servers.append(get_serv)

    def post_handler(self, conn, addr):
        #handle the post request
        content = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE)
            if not buf:
                break
            content += buf
        print(content)
        uid = "32" #TODO
        conn.sendall(uid)

    def get_handler(self, conn, addr):
        #handle the get request
        uid = list()
        while 1:
            buf = conn.recv(SocketServerManager.BUF_SIZE)
            if not buf: 
                break
            uid += buf
        #data = retrieve(uid) #TODO
        data = "kakapout"
        state = conn.sendall(data)
        if state:
            logging.debug('Data not fully transmitted')
            logging.info('The data sent have not been transmitted properly')
            logging.warning('Transmission error')
        conn.close()
        print('Data retrieved')
            
    @staticmethod
    def socket_server_factory(host, port, callback):
        s = socket.getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0)
        return SocketServer(callback, s)

    def run(self):
        for i in self.servers:
            i.start()

class SocketServer(SocketServerManager):
    SEM_MAX = 30
    
    def __init__(self, callback_method, skt):
        self = Process.__init__(self)
        self.skt = skt
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def run(self):
        af, socktype, proto, canonname, sa = self.skt
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None

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
            
        @staticmethod
        def with_sem(f, *args):
            self.sem.acquire()
            f(args)
            self.sem.release()
        
        while 1:
            conn, addr = s.accept()
            with_sem(s.callback, (conn, addr))
            
if __name__ == "__main__":
    SocketServerManager().start()
