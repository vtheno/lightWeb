from os import fstat
from mimetypes import types_map
import os

def make_require_login(handler):
    def require_login(view):
        def _require_login(self, ctx, *args, **kws):
            return handler(view)(self, ctx, *args, **kws)
        return _require_login
    return require_login

def guess_type(filename):
    value = [v for k,v in types_map.items() if filename.endswith(k)]
    if value:
        return 'Content-type', f'{value[0]}'
    return 'Content-type', 'application/octet-stream'

def read_file(filename,access_binary=False) -> "(str,[bytes,str],int) option":
    if os.path.isfile(filename):
        with open(filename,'rb') if access_binary else open(filename,'r',encoding='utf-8') as page:
            content = page.read()
            content_type = guess_type(filename)
            size = 'Content-length', f'{fstat(page.fileno()).st_size}'
        return (content_type,content,size)
    return None

def adjoint(func):
    def warp(*args,**kws):
        ret = func(*args,**kws)
        next(ret)
        return ret
    return warp

__all__ = ["read_file","guess_type","make_require_login","adjoint"]
