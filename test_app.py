#coding=utf-8
from Web.Application import Application
from Web.Request import Request
from Web.httpStatus import *
from Web.Header import *
from Web.Method import *
from Web.Tool import *

from json import dumps
from mimetypes import guess_type
import os
from datetime import datetime
from urllib.parse import quote,unquote

app = Application(__name__)
app.config["root"] = os.getcwd()
app.config["www"] = app.config["root"] + "\\www\\"
app.config["static"] = app.config["www"] + "\\static\\"
app.config["download"] = app.config["www"] + "\\download\\"

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
    content,size = read_file(path)
    ctx.add_header( Content_type("text/html; charset=utf-8") )
    ctx.add_header( Content_length(size) )
    ctx.add_header( Content_encoding("utf-8") )
    ctx.add_header( Content_lang("zh-CN") )
    return ctx.make_response(OK,content)

@app.route("/login")
def login(self, ctx : Request):
    session = app.update_session(ctx)
    method = ctx.get_method()
    if method == GET:
        if session["login"] == False:
            path = app.config["www"] + "login.html"
            content,size = read_file(path)
            ctx.add_general( Cache_Control("no-store") )
            ctx.add_header( Content_encoding("utf-8") )
            ctx.add_header( Content_lang("zh-CN") )
            ctx.add_header( Content_type("text/html; charset=utf-8") )
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

@app.route("/links")
def users(self, ctx : Request):
    session = app.update_session(ctx)
    json = [
        { 'str' : "Home" , 'link' : "/" },
        { 'str' : "Pdf" , 'link' : "/download/test.pdf"  },
        { 'str' : "Jpg" , 'link' : "/download/test.jpg"  },
    ]
    content = str(dumps(json))
    #print(content)
    ctx.add_header( Content_type("application/json") )
    ctx.add_header( Content_length(len(content)) )
    return ctx.make_response(OK,content)

@app.route("/static/{name}")
def static(self, ctx : Request, name : str):
    session = app.update_session(ctx)
    path = app.config["static"] + name
    if os.path.isfile(path):
        with open(path, "rb") as f: # read binary
            size = os.fstat(f.fileno()).st_size
            content_type, encoding = guess_type(path)
            if content_type is None:
                content_type = "application/octet-stream"
            if encoding is not None:
                content_type += f"; charset={encoding}"
            #print( header, size )
            content = f.read()
            ctx.add_header(Content_type(content_type))
            ctx.add_header(Content_length(size))
        return ctx.make_response(OK,content)
    return self.general_route(ctx,name)

@app.route("/download/{name}")
@require_login(app)
def download_name(self, ctx : Request, name : str):
    session = app.update_session(ctx)
    path = app.config["download"] + name
    if os.path.isfile(path):
        with open(path, "rb") as f: # read binary
            size = os.fstat(f.fileno()).st_size
            content_type, encoding = guess_type(path)
            if content_type is None:
                content_type = "application/octet-stream"
            if encoding is not None:
                content_type += f"; charset={encoding}"
            content = f.read()
            ctx.add_header(Content_type(content_type))
            ctx.add_header(Content_length(size))
        return ctx.make_response(OK,content)
    return self.general_route(ctx,name)

@app.route("/{name}")
def hello(self, ctx :Request, name : str):
    session = app.update_session(ctx)
    return ctx.make_response(OK,f"<h1>{name}</h1>")

def redire_to_index(self, ctx : Request):
    session = app.update_session(ctx)
    ctx.add_header( Location("/") )
    return ctx.make_response(Found,'')

app.add_route("/download/",redire_to_index)
app.add_route("/download",redire_to_index)
