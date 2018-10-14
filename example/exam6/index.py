#coding=utf-8
from app import *
from Web.Request import Request
from Web.httpStatus import *
from Web.Header import *
from Web.Method import *
from Web.Tool import *
from Web.View import *

@app.route("/")
@require_login(app)
def index(self, ctx : Request):
    method = ctx.get_method()
    url = ctx.get_url()
    info = ctx.get_info()
    form = ctx.get_form()
    print( "request method =>", method, url)
    print( "request post form =>",form)
    print( "request info =>",info)
    path = app.config["www"] + "index.html"
    content_type,content,size = read_file(path)
    ctx.add_header( Content_type(content_type) )
    ctx.add_header( Content_length(size) )
    ctx.add_header( Content_lang("zh-CN") )
    return ctx.make_response(OK,content)

@app.route("/login")
def login(self, ctx : Request):
    session = app.update_session(ctx)
    method = ctx.get_method()
    if method == GET:
        if session["login"] == False:
            path = app.config["www"] + "login.html"
            content_type,content,size = read_file(path)
            ctx.add_general( Cache_Control("no-store") )
            ctx.add_header( Content_lang("zh-CN") )
            ctx.add_header( Content_type(content_type) )
            ctx.add_header( Content_length(size) )
            return ctx.make_response(OK,content)
        else:
            ctx.add_header( Location("/") )
            return ctx.make_response(Found,'')
    elif method == POST:
        form = ctx.get_form()
        if form["username"] == 'admin' and form["password"] == 'admin':
            session["login"] = True
            session["username"] = form["username"]
        ctx.add_header( Location("/") )
        return ctx.make_response(Found,'')
    else:
        ctx.add_header( Allow("GET,POST") )
        return ctx.make_response(NotAllow,'')

@app.route("/logout")
@allow_method(methods=[GET])
def logout(self, ctx : Request):
    session = app.update_session(ctx) 
    key = session.id
    app.unset_session(key)
    session = app.update_session(ctx) 
    ctx.add_header( Location('/') )
    return ctx.make_response(Found,'')

@app.route("/hi-{name}")
@allow_method(methods=[GET])
def hi(self, ctx, name):
    session = app.update_session(ctx)
    return ctx.make_response(OK,f"hello {name}")

def redire_to_index(self, ctx : Request):
    session = app.update_session(ctx)
    ctx.add_header( Location("/") )
    return ctx.make_response(Found,'')

app.add_route("/download/",redire_to_index)
app.add_route("/download",redire_to_index)

class Hello(metaclass=View):
    def GET(self,ctx:Request,name):
        print( "HELLO GET =>",type(self))
        return ctx.make_response(OK,f"<h2>{name}</h2>")

app.add_route("/hello-{name}",Hello)

__all__ = ["app"]
