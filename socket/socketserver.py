import socket
from multiprocessing import Process
from threading import Semaphore, Thread
import logging
#import ../../

class SocketServerManager(Process):
    BUF_SIZE = 1024
    
    def __init__(self, post_port=1338, get_port=1339, host=None):
        Process.__init__(self)
        self.servers = []
        post_serv = self.socket_server_factory(host, post_port, self.get_handler)
        self.servers.append(post_serv)
        get_serv = self.socket_server_factory(host, get_port, self.post_handler)
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
            
    def socket_server_factory(self, host, port, callback):
        s = socket.getaddrinfo(host, port)
        return SocketServer(callback, s)

    def run(self):
        for s in self.servers[:-2]:
            s.start()
        self.servers[-1].run()

class SocketServer(SocketServerManager):
    SEM_MAX = 30
    
    def __init__(self, callback_method, skt):
        Process.__init__(self)
        self.skt = skt
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def bound(self, s):
        af, socktype, proto, canonname, sa = s
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
            conn, addr = s.accept()
            Thread(target=self.with_sem, args=(s.callback, (conn, addr)))
            
    def run(self):
        threads = []
        for s in self.skt:
            t = Thread(target=self.bound, args=(s, ))
            threads.append(t)
        for t in threads:
            t.join()
            
    def with_sem(self, f, *args):
        self.sem.acquire()
        f(args)
        self.sem.release()
            
if __name__ == "__main__":
    SocketServerManager().start()
