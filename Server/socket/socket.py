from socket import socket
import logging

class SocketServerManager(Process):
    BUF_SIZE = 1024
    def __init__(self, post_port=1338, get_port=1339, host=None):
        self = Process.__init__(self)
        self.servers = []
        self.servers.append(socket_server_factory(host, post_port, self.get_handler))
        self.servers.append(socket_server_factory(host, get_port, self.post_handler))
        self.servers.append(post_serv)

    def run(self)
        #open the two socket and listen to them
        for s in self.servers:
            s.start()
            
    def post_handler(self, conn, addr):
        #handle the post request
        content = list()
        while 1:
            if not data:
                break
            buf = conn.recv(BUF_SIZE)
            content += buf
        data = 
    
    def get_handler(self, conn, addr):
        #handle the get request
        uid = list()
        while 1:
            if not data: 
                break
            buf = conn.recv(BUF_SIZE)
            uid += buf
        data = retrieve(uid)
        state = conn.sendall(data)
        if state: 
            conn.close()
        print 'Data retrieved'
            
    @staticmethod
    def socket_server_factory(host, port, callback):
        s = socket.getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0)
        return SocketServer(callback, s)

    def run(self):
        for i in self.servers:
            i.start()

class SocketServer(SocketServer):
    SEM_MAX = 30
    
    def __init__(self, callback_method, skt):
        self = Process.__init__(self)
        self.skt = skt
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def run(self):
        af, socktype, proto, canonname, sa = self.res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error, msg:
            s = None
            continue

        try:
            s.bind(sa)
            s.listen(1)
        except socket.error, msg:
            #pretty bad
            s.close()
            s = None
            continue
            
        if s is None:
            logging.error("Could not open socket")
            return
            
        @staticmethod
        def with_sem(f, *args):
            self.sem.acquire()
            f(args)
            self.sem.release()
        
        while 1:
            conn, addr = s.accept()
            with_sem(s.callback, (conn, addr))
