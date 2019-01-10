#coding=utf-8
from Web.Request import Request
from Web.Method import Method,methods
from Web.Header import Allow
from Web.HTTPStatus import NotAllow

from types import FunctionType
class View(object):
    __allows__ = ["GET","POST","PUT","HEAD","DELETE","OPTIONS","TRACE","CONNECT"] 
    def __new__(cls, name, bases, attrs, **kws):
        allows = kws.get("allow",[])
        all_allows = [i for i in cls.__allows__ + allows]
        all_method = {k.upper():v for k,v in attrs.items() if k.upper() in all_allows}
        def not_allow(self, ctx, *args, **kws):
            ctx.response.push( str(Allow(','.join(all_method.keys()))) )
            ctx.response.status = str(NotAllow)
            return ctx.response.build_with_string()
        def tranfer(self, ctx, *args, **kws):
            ret = all_method.get(ctx.request.method, not_allow)
            return ret(self, ctx, *args, **kws)
        return tranfer
__all__ = ["View"]
