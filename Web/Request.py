from Web.HTTPStatus import HTTPStatus
from Web.parse import HTTPRequest,HTTPResponse

class Request(object):

    def __init__(self, ctx):
        self.request = HTTPRequest(ctx)
        self.response = HTTPResponse()
    def __repr__(self):
        return "(Request)"

__all__ = ['Request']
