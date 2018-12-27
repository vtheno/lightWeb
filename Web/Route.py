#coding=utf-8
from Web.Request import Request
from Web.HTTPStatus import NotFound
from types import FunctionType
import re
def replace(template: str) -> str:
    pattern = "{(.*?)}"
    result = re.findall(pattern, template)
    ret = template
    for r in result:
        ret = ret.replace('{' + r + '}','(.*)')
    return ret
class Pattern(object):
    def __init__(self,url):
        self.url = url
        self.pattern = replace(self.url)
    def match(self,url):
        ret = re.findall(self.pattern, url)
        if ret:
            result = ret[0]
            return list(result) if isinstance(result,tuple) else [result]
        return None
    def __repr__(self):
        return f'pattern={self.url!r}'
class Route(object):
    def __init__(self,route_table : {Pattern:FunctionType}):
        self.route_table = route_table
    def __repr__(self):
        return repr(self.route_table)
    def route(self, ctx : Request, *args,**kws):
        # route : Request -> Response
        url = ctx.request.url
        for pattern,func in self.route_table.items():
            out = pattern.match(url)
            # print( ">",pattern, out,args,kws )
            if out:
                if out == [url]:
                    return func(self, ctx, *list(args), **kws)
                return func(self, ctx, *(out + list(args)), **kws)
        return self.general_route(ctx, *args, **kws)
    def general_route(self, ctx : Request, *args, **kws):
        return ctx.response.build_with_string(NotFound,"<html><body><h3>404 Page NotFound</h3></body></html>")
__all__ = ["Route","Pattern"]
