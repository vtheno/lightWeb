#coding=utf-8
from Web.Request import Request
from Web.Header import Content_type, Content_length 
from Web.HTTPStatus import Found
from Web.View import View
from Web.Tool import read_file, make_require_login
from app import app

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
#
@app.route("/{pix}")
class Index(metaclass=View):
    def get(self, ctx: Request, pix):
        value = read_file(app.config['www'] + pix + '.png', True)
        if value:
            typ, ctx.response.b_content, size = value
            ctx.response.push( typ )
            ctx.response.push( size )
            return ctx.response.build_with_bytes()
        return self.abort(ctx)

@app.route('/static/{filename}')
class Static(metaclass=View):
    def get(self, ctx: Request, filename):
        value = read_file(app.config['static'] + filename)
        if value:
            typ, ctx.response.content, size = value
            ctx.response.push( typ )
            ctx.response.push( size )
            # ctx.response.push( "Accept-Ranges: bytes" )
            return ctx.response.build_with_string()
        return self.abort(ctx)

@app.route("/login")
def hi(self, ctx):
    ctx.response.content = "hello~"
    ctx.response.push( str(Content_type("text/html")) )
    ctx.response.push( str(Content_length(len(ctx.response.content))) )
    return ctx.response.build_with_string()

@app.route("/reg-{id}")
@require_login
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
