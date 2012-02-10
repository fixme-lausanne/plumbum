from socket import socket


class SocketServerManager(Process):

    def __init__(self, post_port=1338, get_port=1339, host=None):
        self = Process.__init__(self)
        self.servers = []
        self.servers.append(socket_server_factory(host, post_port, self.get_handler))
        self.servers.append(socket_server_factory(host, get_port, self.post_handler))
        self.servers.append(post_serv)

    def run(self)
        #open the two socket and listen to them

            
            
    def post_handler(self, conn, addr):
        #handle the post request
        
    def get_handler(self, conn, addr):
        #handle the get request
        uid = list()
        while 1:
            if not data: break
            buf = conn.recv(1024)
            uid += buf
        data = retrieve(uid)
        state = conn.sendall(data)
        if state:
        conn.close()
        print 'Data retrieved'
=======
    
>>>>>>> 5e0873151389c11fd76e5fc6e540420658d962be
    @staticmethod
    def socket_server_factory(host, port, callback):
        s = socket.getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0)
        return SocketServer(callback, s)

    def run(self):
        for i in self.servers:
            i.start()

    def post_handler(self, conn, addr):
        #handle the post request

    def get_handler(self, conn, addr):
        #handle the get request

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
            print("Could not open socket")
            return
            
        while 1:
            
<<<<<<< HEAD
            conn, addr = s.accept()
            s.callback(conn, addr)
=======
>>>>>>> 6e77d8a0c0d98c863952f010dd3eff3b5d358d40
>>>>>>> 5e0873151389c11fd76e5fc6e540420658d962be
