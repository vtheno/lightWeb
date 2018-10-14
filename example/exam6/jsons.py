#coding=utf-8
from app import app

from Web.Request import Request
from Web.Header import *
from Web.httpStatus import *

from json import dumps

@app.route("/links")
def links(self, ctx : Request):
    session = app.update_session(ctx)
    json = [
        { 'str' : "Home" , 'link' : "/" },
        { 'str' : "Pdf" , 'link' : "/download/test.pdf"  },
        { 'str' : "Jpg" , 'link' : "/download/test.jpg"  },
    ]
    content = str(dumps(json))
    ctx.add_header( Content_type("application/json") )
    ctx.add_header( Content_length(len(content)) )
    return ctx.make_response(OK,content)

__all__ = ["app"]
