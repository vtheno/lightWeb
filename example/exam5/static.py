#coding=utf-8
from app import app

from Web.Request import Request
from Web.Header import *
from Web.httpStatus import *
from Web.Tool import *

@app.route("/static/{name}")
def static(self, ctx : Request, name : str):
    app.update_session(ctx)
    path = app.config["static"] + name
    value = read_file(path,True)
    if value:
        content_type,content,size = value
        ctx.add_header(Content_type(content_type))
        ctx.add_header(Content_length(size))
        return ctx.make_response(OK,content)
    return self.general_route(ctx,name)

__all__ = ["app"]
