#coding=utf-8
from Web.Request import *
from Web.Header import *
from Web.View import *
from Web.Tool import *
from Web.HTTPStatus import OK
from app import app

@app.route("/static/{filename}")
class StaticFile(metaclass=View):
    def GET(self,ctx:Request,filename):
        path = app.config["root"] + filename
        value = read_file(path)
        if value:
            typ,content,length = value
            ctx.add_header(Content_type(typ))
            ctx.add_header(Content_length(length))
            return ctx.make_response(OK,content)
        return self.general_route(ctx)

from json import dumps
@app.route("/links")
class Links(metaclass=View):
    def get(self, ctx:Request):
        data = [{
            "/url1":"value1",
            "/url2":"value2",
            "/urln":"valuen",
        }]
        content = str(dumps(data))
        ctx.add_header( Content_type("application/json") )
        ctx.add_header( Content_length(len(content)) )
        return ctx.make_response(OK,content)
@app.route("/")
class Index(metaclass=View):
    def get(self, ctx: Request):
        content = "Hello World!"
        ctx.add_header( Content_type("text/html") )
        ctx.add_header( Content_length(len(content)) )
        return ctx.make_response(OK,content)
__all__ = ["app"]
