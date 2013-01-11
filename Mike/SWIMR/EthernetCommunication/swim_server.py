# Echo server program
import SocketServer
import sys

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data
        socket.sendto(data.upper(), self.client_address)
        self.DATA = data
    
        
        

if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    if HOST is None or PORT is None:
        print "try again stupid: python swim_server.py 153.106.75.171 9999"
        exit(1)
    # HOST, PORT = "153.106.113.107", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    #server.serve_forever()
    server.handle_request()
    print server.RequestHandlerClass.DATA
    