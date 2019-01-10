#coding=utf-8
from Web.Request import Request
from Web.Header import Content_type, Content_length 
from Web.HTTPStatus import Found
from Web.View import View
from app import app

def make_require_login(handler):
    def require_login(view):
        def _require_login(self, ctx, *args, **kws):
            return handler(view)(self, ctx, *args, **kws)
        return _require_login
    return require_login

def handler(view):
    def _(self, ctx, *args, **kws):
        session = self.sessions.update_session(ctx)
        print( 'handler', session )
        if session and session["login"]:
            return view(self, ctx, *args,**kws)
        ctx.response.push( 'Location: /login' )
        ctx.response.status = str(Found)
        print( ctx.response.status )
        return ctx.response.build_with_string()
    return _

require_login = make_require_login(handler)
#@require_login
@app.route("/")
class Index(metaclass=View):
    def get(self, ctx: Request):
        ctx.response.content = "index!"
        ctx.response.push( str(Content_type("text/html")) )
        ctx.response.push( str(Content_length(len(ctx.response.content))) )
        resp = ctx.response.build_with_string()
        return resp
@app.route("/login")
def hi(self, ctx):
    ctx.response.content = "hello~"
    ctx.response.push( str(Content_type("text/html")) )
    ctx.response.push( str(Content_length(len(ctx.response.content))) )
    return ctx.response.build_with_string()

@app.route("/reg-{id}")
class Register(metaclass=View):
    def get(self, ctx: Request, id):
        print( id )
        ctx.response.content = "register"
        ctx.response.push( str(Content_type("text/html")) )
        ctx.response.push( str(Content_length(len(ctx.response.content))) )
        return ctx.response.build_with_string()
    def post(self, ctx: Request, id):
        ctx.request.parseForm()
        print( ctx.request.form )
        ctx.response.content = str(ctx.request.form)
        ctx.response.push( str(Content_type("text/plain")) )
        ctx.response.push( str(Content_length(len(ctx.response.content))) )
        return ctx.response.build_with_string()
__all__ = ["app"]
