#coding=utf-8
from Web.Application import Application
from Web.Request import Request
from Web.httpStatus import *

from json import dumps
from mimetypes import guess_type
import os

app = Application(__name__)
app.config["root"] = os.getcwd()
app.config["static"] = app.config["root"] + "\\static\\"

@app.route("/")
def index(self, ctx : Request):
    return ctx.make_response(OK,"<title>Test</title><h1>Hello World!</h1>")
@app.route("/hi-{name}")
def hi(self, ctx, name):
    return ctx.make_response(OK,f"hello {name}")
@app.route("/users")
def users(self, ctx : Request):
    json = [
        { 'str' : "Home" , 'link' : "#" },
        { 'str' : "Github" , 'link' : "##" },
        { 'str' : "Download" , 'link' : "###"  },
    ]
    content = str(dumps(json))
    #print(content)
    ctx.add_header("Content-type: application/json")
    return ctx.make_response(OK,content)
    
@app.route("/static/{name}")
def static(self, ctx : Request, name : str):
    path = app.config["static"] + name
    if os.path.isfile(path):
        with open(path, "rb") as f: # read binary
            stat = os.fstat(f.fileno())
            size = stat.st_size
            content_type, encoding = guess_type(path)
            header = "Content-type: "
            if content_type is None:
                content_type = "application/octet-stream"
            if encoding is not None:
                content_type += f"; charset={encoding}"
            header += content_type
            #print( header, size )
            content = f.read()
            ctx.add_header(header)
            ctx.add_resp(f"Content-length: {size}")
        return ctx.make_response(OK,content)
    return self.general_route(ctx,name)

