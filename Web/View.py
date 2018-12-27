#coding=utf-8
from Web.Request import Request
from Web.Method import Method,methods
from Web.Header import Allow
from Web.HTTPStatus import NotAllow

from types import FunctionType

def choice_method(env : {Method:FunctionType}):
    #print ( env )
    def warp_choice(self, ctx : Request,*args,**kws):
        method = ctx.request.method
        for k,v in env.items():
            if method == k:
                #print( v )
                return v(self,ctx,*args,**kws)
        ctx.response.push( str(Allow(','.join(env.keys()))) )
        return ctx.response.build_with_string(NotAllow,'')
    return warp_choice
class View(type):
    def __new__(cls,name,parents,attrs):
        env = {k.upper():v for k,v in attrs.items() if k.upper() in methods}
        return choice_method(env)
__all__ = ["View"]
