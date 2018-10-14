from Web.Header import Location,Allow
from Web.httpStatus import Found,NotAllow

import os
from os import fstat
from mimetypes import guess_type

def require_login(app : "Application"):
    def _warp_login(func):
        def warp_login(self, ctx :"Request", *args,**kws):
            session = app.update_session(ctx)
            if session and session["login"]:
                return func(self, ctx, *args,**kws)
            ctx.add_header( Location("/login") )
            return ctx.make_response(Found,'')
        return warp_login
    return _warp_login

def allow_method(methods:[str]):
    def _warp_allow(func):
        def warp_allow(self, ctx : "Request", *args,**kws):
            if ctx.get_method() in methods:
                return func(self, ctx, *args, **kws)
            else:
                ctx.add_header( Allow(','.join(methods)) )
                return ctx.make_response(NotAllow,'')
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


__all__ = ["require_login","read_file","allow_method","call"]
