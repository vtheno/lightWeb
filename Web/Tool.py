from Web.Header import Location,Allow
from Web.HTTPStatus import Found,NotAllow

import os
from os import fstat
from mimetypes import guess_type

def require_login(app : "Application"):
    def _warp_login(func):
        def warp_login(self, ctx :"Request", *args,**kws):
            session = app.update_session(ctx)
            if session and session["login"]:
                return func(self, ctx, *args,**kws)
            ctx.response.push( str(Location("/login")) )
            return ctx.response.build_with_string(str(Found),'')
        return warp_login
    return _warp_login

def allow_method(methods:[str]):
    def _warp_allow(func):
        def warp_allow(self, ctx : "Request", *args,**kws):
            if ctx.request.method in methods:
                return func(self, ctx, *args, **kws)
            else:
                ctx.response.push( str(Allow(','.join(methods))) )
                return ctx.response.build_with_string(str(NotAllow),'')
        return warp_allow
    return _warp_allow

def call(func):
    return func()

def read_file(filename,access_binary=False) -> [None,(str,[bytes,str],int)]:
    if os.path.isfile(filename):
        with open(filename,'rb') if access_binary else open(filename,'r',encoding='utf-8') as page:
            content = page.read()
            content_type, encoding = guess_type(filename)
            if content_type is None:
                content_type = "application/octet-stream"
            if encoding is not None:
                content_type += f"; charset={encoding}"
            size = fstat(page.fileno()).st_size
        return (content_type,content,size)
    return None

def adjoint(func):
    def warp(*args,**kws):
        ret = func(*args,**kws)
        next(ret)
        return ret
    return warp
def Split(inp: str,target=' '):
    temp = ''
    i = 0
    length = len(inp)
    while i < length:
        if inp[i] == target:
            if temp:
                yield temp
                temp = ''
        else:
            temp += inp[i]
        i += 1
    if temp:
        yield temp
__all__ = ["require_login","read_file","allow_method","call","adjoint","Split"]
