from Web.HTTPStatus import HTTPStatus
from Web.parse import HTTPRequest,HTTPResponse

from urllib.parse import quote, unquote
from html import escape

class Request(object):

    def __init__(self, ctx):
        #print( ctx )
        self.ctx = ctx # client_recv_buff
        self.request = HTTPRequest(self.ctx)
        # self.request.parseForm()
        self.response = HTTPResponse()
    def __repr__(self):
        return repr(self.ctx)

__all__ = ['Request']
