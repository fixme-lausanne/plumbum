from socket import socket

Class SocketServerManager(Process):

    def __init__(self, post_port=1338, get_port=1339, host=None):
        self = Process.__init__(self)
        self.servers = []
        self.servers.append(socket_server_factory(host, post_port, self.get_handler))
        self.servers.append(socket_server_factory(host, get_port, self.post_handler))
        self.servers.append(post_serv)

    @staticmethod
    def socket_server_factory(host, port, callback):
        s = socket.getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0)
        return SocketServer(callback, s)

    def run(self):
        for i in self.servers:
            i.start()

    def post_handler():
        #handle the post request

    def get_handler():
        #handle the get request

class SocketServer(SocketServer):
    SEM_MAX = 30

    def __init__(self, callback_method, skt):
        self = Process.__init__(self)
        self.skt = skt
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def run(self):
        s.listen()
        while 1:
            addr = s.listen(1)
            s.callback()
