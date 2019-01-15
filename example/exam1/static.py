#coding=utf-8
from Web.Request import Request
from Web.HTTPStatus import Status
from Web.View import View
from Web.Tool import read_file, make_require_login
from app import app

def handler(view):
    def _(self, ctx, *args, **kws):
        session = self.sessions.update_session(ctx)
        if session and session["login"]:
            return view(self, ctx, *args,**kws)
        ctx.response.status = Status[302]
        ctx.response.push( 'Location', '/login' )
        return ctx.response.build_with_string()
    return _

require_login = make_require_login(handler)
# important about "/{ url }" pattern it replace all url
# drop Content_length etc...
# modify push(obj) to push(key, value)
# claim program @xxx it'll fast!
@app.route("/pix/{pix}")
class Index(metaclass=View):
    def get(self, ctx: Request, pix):
        value = read_file(app.config['www'] + pix + '.png', True)
        if value:
            typ, ctx.response.b_content, size = value
            ctx.response.push( *typ )
            ctx.response.push( *size )
            return ctx.response.build_with_bytes()
        return self.abort(ctx)
# api
import json
@app.route("/data")
class Data(metaclass=View):
    def get(self, ctx: Request):
        data = [{
            "id": "1",
            "content": "first item"
        }]
        ctx.response.content = json.dumps(data)
        ctx.response.push( 'Content-type', 'application/json')
        ctx.response.push( 'Content-length', f'{len(ctx.response.content)}')
        ctx.response.push( 'Access-Control-Allow-Origin', '*' )
        return ctx.response.build_with_string()
@app.route("/search")
class Search(metaclass=View):
    def options(self, ctx: Request):
        print(ctx.request.info)
        ctx.response.push( 'Access-Control-Allow-Origin', '*' )
        ctx.response.push( 'Access-Control-Request-Methods',' POST, OPTIONS')
        ctx.response.push( 'Access-Control-Allow-Headers','Content-Type')
        return ctx.response.build_with_bytes()
    def post(self, ctx: Request):
        ctx.request.parseForm_with_json()
        print( ctx.request.form )
        data = [{
            "id": "1",
            "content": "first item"
        }]
        ctx.response.content = json.dumps(data)
        ctx.response.push( 'Content-type', 'application/json')
        ctx.response.push( 'Content-length', f'{len(ctx.response.content)}')
        ctx.response.push( 'Access-Control-Allow-Origin', '*' )
        return ctx.response.build_with_string()

@app.route('/static/{filename}')
class Static(metaclass=View):
    def get(self, ctx: Request, filename):
        value = read_file(app.config['static'] + filename)
        if value:
            typ, ctx.response.content, size = value
            ctx.response.push( *typ )
            ctx.response.push( *size )
            # ctx.response.push( "Accept-Ranges: bytes" )
            return ctx.response.build_with_string()
        return self.abort(ctx)

@app.route("/login")
def hi(self, ctx):
    ctx.response.content = "hello~"
    ctx.response.push( 'Content-type', "text/html" )
    ctx.response.push( 'Content-length', f'{len(ctx.response.content)}')
    return ctx.response.build_with_string()

@app.route("/register-{id}")
@require_login
class Register(metaclass=View):
    def get(self, ctx: Request, id):
        print( id )
        ctx.response.content = "register"
        ctx.response.push( 'Content-type', "text/html" )
        ctx.response.push( 'Content-length', f'{len(ctx.response.content)}')
        return ctx.response.build_with_string()
    def post(self, ctx: Request, id):
        ctx.request.parseForm_with_url()
        print( ctx.request.form )
        ctx.response.content = str(ctx.request.form)
        ctx.response.push( 'Content-type', "text/plain" )
        ctx.response.push( 'Content-length', f'{len(ctx.response.content)}')
        return ctx.response.build_with_string()

__all__ = ["app"]
