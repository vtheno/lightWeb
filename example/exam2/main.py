#coding=utf-8
from Web.Server import HTTPServer
from Web.Tool import call

from app import app
from static import app

@call
@call
def _():
    return HTTPServer(app,'localhost',80).run_forever
