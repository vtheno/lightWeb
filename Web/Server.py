#coding=utf-8
from Web.Request import Request
from Web.Log import *
from Web.Tool import adjoint
from traceback import TracebackException
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, Executor
import threading
import socket

def error_trace(e):
    # from traceback.print_exc
    limit = None
    chain = True
    tb = e.__traceback__
    value = e
    etype = type(e)
    out = [ ]
    for line in TracebackException(type(value), value, tb, limit=limit).format(chain=chain):
        out += [line.strip("\n")]
    return '; '.join(out[-2:])

class HTTPServer(object):
    def __init__(self,app,host:str,port:int,logname='lightWeb.log'):
        self.app = app
        self.host = host
        self.port = port
        self.log = Log(logname)
    def __repr__(self):
        return f"{self.host}:{self.port} => {self.app}"
    def handler(self, obj):
        client_sock,client_addr = obj
        # print( client_addr, client_sock )
        try:
            with client_sock:
                #buff = str(client_sock.recv(16_384), 'iso-8859-1')
                buff = client_sock.recv(16_384).decode('utf-8')
                if buff:
                    request = Request(buff)
                    resp = self.app.lookup(request)
                    client_sock.sendall(resp)
                    self.log.info(f"{client_addr} => {request}")
                else:
                    client_sock.shutdown(socket.SHUT_WR)
        except Exception as e:
            # write log
            self.log.error(f"Handler Error => {error_trace(e)}")
        finally:
            client_sock.close()
    def start(self, worker=1024):
        print( f"Server Listening on {self.host}:{self.port} ..." )
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET,
                            socket.SO_REUSEADDR,
                            1)
            sock.bind((self.host, self.port))
            sock.setblocking( False )
            sock.listen(worker)
            sock.settimeout(0.002)
            with ThreadPoolExecutor(max_workers=worker) as pool:
                while 1:
                    try:
                        pool.submit(self.handler, sock.accept())
                    except socket.timeout:
                        continue
                    except Exception as e:
                        self.log.error(f"Server Error => {error_trace(e)}")
                        continue
__all__ = ["HTTPServer"]
