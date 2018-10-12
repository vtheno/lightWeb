#coding=utf-8
from Web.Request import Request
from Web.httpStatus import NotFound

from types import FunctionType
class Pattern(object):
    def __init__(self,url):
        self.url = url.split("/")
        #self.url_str = url
    def get_pattern(self,s):
        out = [ ]
        inline = [ ]
        current = out
        for i in s:
            if i == "}":
                current = out
            elif i == "{":
                current += [None]
                current = inline
            else:
                current += [i]
        if None in out:
            idx = out.index(None)
            left = ''.join(out[:idx])
            right = ''.join(out[idx+1:])
            name = ''.join(inline)
            return lambda url:self.equal(left,name,right,url)
        else:
            return lambda _:False
    def equal(self,left,center,right,url):
        l = len(left)
        r = len(right)
        dif = len(url) - (l + r)
        drop_left,out,drop_right = url[0:l],url[l:l+dif],url[l+dif:]
        if drop_left == left and drop_right == right:
            return out
        return False
    def match(self,url):
        #print( "match =>",self.url_str,url)
        url = url.split("/")
        #print( "match =>",self.url,url)
        args = [ ]
        if len(url) != len(self.url):
            return False
        for p,v in zip(self.url,url):
            if p == v:
                continue
            else:
                out = self.get_pattern(p)(v)
                if out != False and out:
                    args += [out]
                    continue
                else:
                    return False
        return args
    def __repr__(self):
        return f'pattern={"/".join(self.url)!r}'
class Route(object):
    def __init__(self,route_table : {Pattern:FunctionType}):
        self.route_table = route_table
    def __repr__(self):
        return repr(self.route_table)
    def route(self, ctx : Request, *args,**kws):
        # route : Request -> Response
        #from pprint import pprint
        #pprint( self.route_table )
        url = ctx.get_url ()
        #print( "Route:", url )
        for pattern,func in self.route_table.items():
            out = pattern.match(url)
            #print( "out =>",out )
            if out != False:
                return func(self, ctx, *(out + list(args)), **kws)
        else:
            return self.general_route(ctx, *args, **kws)
    def general_route(self, ctx : Request, *args, **kws):
        return ctx.make_response(NotFound,"<html><body><h3>Page NotFound</h3></body></html>")
__all__ = ["Route","Pattern"]
