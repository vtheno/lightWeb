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
            ctx.response.push(str(Content_type(typ)))
            ctx.response.push(str(Content_length(length)))
            return ctx.response.build_with_string(OK,content)
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
        ctx.response.push( str(Content_type("application/json")) )
        ctx.response.push( str(Content_length(len(content))) )
        return ctx.response.build_with_string(OK,content)
@app.route("/")
class Index(metaclass=View):
    def get(self, ctx: Request):
        content = "Hello World!"
        ctx.response.push( str(Content_type("text/html")) )
        ctx.response.push( str(Content_length(len(content))) )
        resp = ctx.response.build_with_string(OK,content)
        # print( ctx.response.headers )
        # print( resp )
        return resp
__all__ = ["app"]
