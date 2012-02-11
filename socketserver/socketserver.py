import socket
from multiprocessing import Process
from threading import Semaphore, Thread
import logging


class SocketServerManager():
    BUF_SIZE = 1024

    def __init__(self, post_port=1338, get_port=1339, host=None):
        Process.__init__(self)
        self.post_port = post_port
        self.get_port = get_port
        self.host = host
        self.servers = []
        post_serv = self.socket_server_factory(self.host, self.post_port, self.get_handler)
        self.servers.append(post_serv)
        get_serv = self.socket_server_factory(self.host, self.get_port, self.post_handler)
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
        conn.sendall(uid.encode('UTF-8'))

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
        state = conn.sendall(data.encode("UTF-8"))
        if state:
            logging.debug('Data not fully transmitted')
            logging.info('The data sent have not been transmitted properly')
            logging.warning('Transmission error')
        conn.close()
        print('Data retrieved')

    def socket_server_factory(self, host, port, callback):
        s = socket.getaddrinfo(host, port)
        server = SocketServer(callback, s)
        return server

    def run(self):
        for s in self.servers:
            s.start()
        for s in self.servers:
            s.join()

class SocketServer(Process):
    SEM_MAX = 30

    def __init__(self, callback_method, skt):
        Process.__init__(self)
        self.callback = callback_method
        self.skt = skt
        self.sem = Semaphore(SocketServer.SEM_MAX)

    def bound(self, s):
        af, socktype, proto, canonname, sa = s
        print(s)
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            return

        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            #pretty bad
            logging.error(msg)
            s.close()
            return 

        while 1:
            print("CONNECTION")
            acc = s.accept()
            t = Thread(target=self.with_sem, args=(self.callback, acc))
            t.run()

    def run(self):
        threads = []
        for s in self.skt:
            t = Thread(target=self.bound, args=(s, ))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    def with_sem(self, f, arg):
        self.sem.acquire()
        f(arg[0], arg[1])
        self.sem.release()

if __name__ == "__main__":
    SocketServerManager().run()
