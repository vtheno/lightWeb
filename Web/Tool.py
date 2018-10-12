from Web.Header import Location,Allow
from Web.httpStatus import Found,NotAllow

from os import fstat

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

def read_file(filename):
    with open(filename,'r',encoding='utf-8') as page:
        content = page.read()
        size = fstat(page.fileno()).st_size
    return (content,size)


__all__ = ["require_login","read_file","allow_method","call"]
