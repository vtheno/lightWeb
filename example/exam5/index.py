#coding=utf-8
from Web.Request import Request
from Web.httpStatus import *
from Web.Header import *
from Web.Method import *
from Web.Tool import *
from Web.View import *

from app import *
from generate import *
@app.route("/")
class Index(metaclass=View):
    def GET(self,ctx:Request):
        app.update_session(ctx)
        value = read_file(app.config["www"] + "index.html")
        if value:
            typ,cont,size = value
            ctx.add_header( Content_type(typ) )
            ctx.add_header( Content_length(size) )
            return ctx.make_response(OK,cont)
        return self.general_route(ctx)
@app.route("/hi")
class Hi(metaclass=View):
    def GET(self,ctx:Request):
        style = grid_style(10,10)
        js = vueJS([
            Data(0,0,'lightblue','hello'),
            ])
        page = html("hi",[],
                    [
                        'vue/vue.js',
                        'vue/vue-resource@1.5.1',
                    ],
                    inlineStyle(style),inlineJS(js))
        size = len(page)
        ctx.add_header( Content_type('text/html') )
        ctx.add_header( Content_length(size) )
        return ctx.make_response(OK,page)
__all__ = ["app"]
