import socket 

Class SocketServer(Process):
    def __init__(self, post_port=1338, get_port=1339):
        
        
    def run(self, )
        #open the two socket and listen to them
        post_socket = socket.create_connexion()
        get_socket = socket
        while 1:
            
            
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
        conn.senall(data)
        conn.close()
        print 'Data retrieved'
