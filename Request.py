from httpStatus import HttpStatus
from urllib.parse import quote, unquote
from html import escape
from Check import AssertCheck

class Request(object):

    def __init__(self, ctx):
        AssertCheck(ctx, str)
        self.ctx = ctx
        self.first = []
        self.header = []
        self.resp = []
        self._ctx_msg, self._ctx_forms = self.ctx.split('\r\n\r\n')
        self._ctx_method_route_version, *self._ctx_infos = [i for i in self._ctx_msg.split('\r\n') if i]
        self._ctx_forms = [i for i in self._ctx_forms.split('\r\n') if i]

    def __repr__(self):
        return repr(self.ctx)

    def get_info(self):
        table = dict([tuple(o.split(': ')) for o in self._ctx_infos])
        return table

    def get_form(self):
        table = dict([tuple(unquote(r).split('&')) for r in self._ctx_forms])
        return table

    def get_url(self):
        method, route, http_version = self._ctx_method_route_version.split()
        route = escape(unquote(route, encoding='utf-8'), quote=1)
        return route

    def get_method(self):
        method, route, http_version = self.method_route_version.split()
        return method

    def add_first(self, first):
        AssertCheck(first, str)
        self.first += [first + '\r\n']

    def add_header(self, header):
        AssertCheck(header, str)
        self.header += [header + '\r\n']

    def add_resp(self, resp):
        AssertCheck(resp, str)
        self.resp += [resp + '\r\n']

    def make_response(self, status, content):
        AssertCheck(status, HttpStatus)
        if isinstance(content, bytes) or isinstance(content, str):
            AssertCheck(content, type(content))
        self.add_first(f'''HTTP/1.1 {status!s}''')
        self.add_resp('')
        if isinstance(content, str):
            self.add_resp(content)
        response = ''
        for first in self.first:
            response += first

        for header in self.header:
            response += header

        for resp in self.resp:
            response += resp

        response = response.encode()
        if isinstance(content, str):
            return bytes(response)
        else:
            return bytes(response) + content

__all__ = ['Request']
