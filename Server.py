#coding=utf-8
import socket
from urllib.parse import quote,unquote
from Request import Request
class HTTPServer(object):
    def __init__(self,app,host,port):
        self.app = app
        self.host = host
        self.port = port
    def __repr__(self):
        return f"{self.host}:{self.port} => {self.app}"
    def application(self,client_sock):
        with client_sock:
            buff = str(client_sock.recv(16_384), 'iso-8859-1')
            if buff:
                request = Request(buff)
                resp = self.app.lookup(request)
                client_sock.sendall(resp)
            else:
                client_sock.sendall(buff)
    def start(self):
        print( f"Server Listening on {self.host}:{self.port} ..." )
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET,
                                 socket.SO_REUSEADDR,
                                 1)
            sock.bind((self.host, self.port))
            sock.setblocking( False )
            sock.listen(1024)
            sock.settimeout(0.002)
            while 1:
                try:
                    try:
                        client_sock,client_addr = sock.accept()
                        self.application(client_sock)
                    except socket.timeout:
                        continue
                    except Exception:
                        continue
                except KeyboardInterrupt:
                    print( f"Server shutdown" )
                    break

__all__ = ["HTTPServer"]
