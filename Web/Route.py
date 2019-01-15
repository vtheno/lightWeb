#coding=utf-8
from Web.Request import Request
from Web.HTTPStatus import Status
from Web.Session import Sessions
from types import FunctionType

class Route(object):
    def __init__(self,route_table: {'reg str': FunctionType} ):
        self.route_table = route_table
        self.sessions = Sessions()
    def __repr__(self):
        return repr(self.route_table)
    def lookup(self, ctx : Request): 
        for k,v in self.route_table.items():
            value = k.match(ctx.request.url)
            if value:
                print( f'{ctx.request.method} {ctx.request.url}' )
                return v(self, ctx, **value.groupdict())
        return self.abort(ctx)
    def abort(self, ctx : Request): 
        ctx.response.status = Status[404]
        ctx.response.content = "<html><body><h3>404 Page NotFound</h3></body></html>"
        return ctx.response.build_with_string()

__all__ = ["Route"]
