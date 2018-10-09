#coding=utf-8
from Web.Server import HTTPServer
from test_app import app

from pprint import pprint

server = HTTPServer(app,'0.0.0.0',80)
#pprint( app.config )
print( "--------------------------------------------------" )
pprint( app._route.route_table )
print( "--------------------------------------------------" )
#pprint( server )
server.run_forever()
