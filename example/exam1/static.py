#coding=utf-8
from Web.Request import *
from Web.Header import *
from Web.View import *
from Web.Tool import *
from Web.httpStatus import OK
from app import app

@app.route("/{filename}")
class StaticFile(metaclass=View):
    def GET(self,ctx:Request,filename):
        path = app.config["root"] + filename
        print( "path =>",path )
        typ,content,length = read_file(path)
        ctx.add_header(Content_type(typ))
        ctx.add_header(Content_length(length))
        return ctx.make_response(OK,content)

__all__ = ["app"]
