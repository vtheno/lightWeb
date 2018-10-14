#coding=utf-8
from Web.Request import Request
from Web.Log import *

import socket
from urllib.parse import quote,unquote
import os,threading,time,subprocess,sys
from pprint import pprint
from traceback import TracebackException

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
    def __init__(self,app,host:str,port:int):
        self.app = app
        self.host = host
        self.port = port
    def __repr__(self):
        return f"{self.host}:{self.port} => {self.app}"
    def application(self,client_sock,client_addr):
        try:
            with client_sock:
                buff = str(client_sock.recv(16_384), 'iso-8859-1')
                if buff:
                    request = Request(buff)
                    Log.info(f"{client_addr} => {request}")
                    resp = self.app.lookup(request)
                    client_sock.sendall(resp)
        except Exception as e:
            # write log
            Log.error(f"server error => {error_trace(e)}")
            return 
    def start(self):
        print( f"Server Listening on {self.host}:{self.port} ..." )
        threading._start_new_thread(self.app.gc_session,())
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
                    client_sock,client_addr = sock.accept()
                    threading._start_new_thread(self.application,(client_sock,client_addr))
                except socket.timeout:
                    continue
                except Exception as e:
                    # write log 
                    Log.error(f"server error => {error_trace(e)}")
                    continue
    def have_file_changed(self):
        FILES = {i.__file__:i for i in sys.modules.values() if getattr(i,"__file__",False)}
        FILE_MTIME_MODULES = {name:(os.path.getmtime(name),module) for name,module in FILES.items()}
        while 1:
            for filename,mtime_module in FILE_MTIME_MODULES.items():
                mtime,module = mtime_module
                cur_time = os.path.getmtime(filename)
                if cur_time != mtime:
                    print( "\033[2J\033m" ) # clear
                    print( "reload file => ",filename,mtime,cur_time )
                    sys.exit(233)
            time.sleep(1)
    def run_forever(self):
        try:
            if os.environ.get('reload') == 'true':
                threading._start_new_thread(self.start,())
                self.have_file_changed()
            else: # first step in there ... 
                while 1:
                    os.environ['reload'] = 'true'
                    args = [sys.executable]+sys.argv
                    flag = subprocess.call(args,env=os.environ)
                    print( f"flag: {flag}" )
                    if flag != 233:
                        sys.exit( flag )
        except KeyboardInterrupt:
            return 
__all__ = ["HTTPServer"]
