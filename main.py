#coding=utf-8
from Web.Server import HTTPServer
from Web.Tool import call
from test_app import app

from pprint import pprint

server = HTTPServer(app,'0.0.0.0',80)
@print
@call
def _():
    return "--------------------------------------------------"
@pprint
@call
def _():
    return app._route.route_table
@print
@call
def _():
    return "--------------------------------------------------"
@call
@call
def _():
    return server.run_forever
