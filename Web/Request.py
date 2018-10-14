from Web.httpStatus import HttpStatus

from urllib.parse import quote, unquote
from html import escape

class Request(object):

    def __init__(self, ctx):
        #print( ctx )
        self.ctx = ctx # client_recv_buff
        self.always = []
        self.general = []
        self.header = []
        self.resp = []
        self._ctx_msg, self._ctx_forms = self.ctx.split('\r\n\r\n')
        self._ctx_method_route_version, *self._ctx_infos = [i for i in self._ctx_msg.split('\r\n') if i]

    def __repr__(self):
        return repr(self.ctx)

    def get_info(self):
        table = [tuple(o.split(': ')) for o in self._ctx_infos]
        table = [(k.lower(),v) for k,v in table]
        return dict(table)

    def get_session_key(self):
        cookie = self.get_info().get("cookie")
        if cookie:
            key,value = tuple(cookie.split("="))
            if key == "session" and value:
                return value
        return None

    def get_form(self):
        table = [tuple(i.split("=")) for i in self._ctx_forms.split("&") if i]
        return dict(table)

    def get_url(self):
        method, route, http_version = self._ctx_method_route_version.split()
        #route = escape(unquote(route, encoding='utf-8'), quote=1)
        route = unquote(route,encoding='utf-8')
        # print( f"route => {route}" )
        return route

    def get_method(self):
        method, route, http_version = self._ctx_method_route_version.split()
        return method.upper()

    def add_always(self, always : str):
        self.always += [always + '\r\n']

    def add_general(self, general : str):
        self.general += [general + '\r\n']

    def add_header(self, header : str):
        self.header += [header + '\r\n']

    def add_resp(self, resp : str):
        self.resp += [resp + '\r\n']

    def make_response(self, status : HttpStatus, content : [str,bytes]):
        self.add_always(f'''HTTP/1.1 {status!s}''')
        self.add_always("Server: ligthWeb")
        self.add_resp('')
        if isinstance(content, str):
            self.add_resp(content)
        response = ''
        for always in self.always:
            response += always

        for general in self.general:
            response += general

        for header in self.header:
            response += header

        for resp in self.resp:
            response += resp

        response = response.encode('utf-8')
        if isinstance(content, str):
            return bytes(response)
        else:
            return bytes(response) + content

__all__ = ['Request']
