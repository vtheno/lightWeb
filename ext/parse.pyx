
cdef class HTTPRequest:
    #self._ctx_msg, self._ctx_forms = self.ctx.split('\r\n\r\n')
    #self._ctx_method_route_version, *self._ctx_infos = [i for i in self._ctx_msg.split('\r\n') if i]
    #self.info = dict((k.lower(),v) for k,v in (tuple(o.split(': ')) for o in self._ctx_infos))
    #self.form = dict(tuple(i.split("=")) for i in self._ctx_forms.split("&") if i)
    cpdef str msg
    cpdef str forms
    cpdef str method_route_version
    cpdef list infos
    cpdef public str method
    cpdef public str url
    cpdef public str http_version
    cpdef public dict info
    cpdef public dict form
    cpdef void parse(self, str inp):
        self.msg, self.forms = inp.split("\r\n\r\n")
        self.method_route_version, *self.infos = [i for i in self.msg.split("\r\n") if i]
        self.method, self.url, self.http_version = self.method_route_version.split()
        self.method = self.method.upper()
        self.info = dict([(k.lower(),v) for k,v in [tuple(o.split(': ')) for o in self.infos]])
        self.form = dict([tuple(i.split("=")) for i in self.forms.split("&") if i])
    cpdef object get_session(self):
        cookie = self.info.get("cookie")
        if cookie:
            key,value = tuple(cookie.split("="))
            if key == "session" and value:
                return value
        return None

cdef class HTTPResponse:
    cpdef public list headers
    def __init__(self):
        self.headers = []
    cpdef void push(self, str header):
        self.headers.append(header)
    cpdef void remove(self, str header):
        self.headers.remove(header)
    cpdef bytes build_with_string(self, object status, str content):
        cpdef str buff
        buff = '\r\n'.join([
            f"HTTP/1.1 {status!s}",
            "Server: lightWeb"
        ]) + "\r\n"
        buff += '\r\n'.join(self.headers) + "\r\n\r\n"
        buff += content
        return bytes(buff, 'utf-8')
    cpdef bytes build_with_bytes(self, object status, bytes content):
        cpdef str buff
        buff = '\r\n'.join([
            f"HTTP/1.1 {status!s}",
            "Server: lightWeb"
        ]) + "\r\n"
        buff += '\r\n'.join(self.headers) + "\r\n\r\n"
        return bytes(buff, 'utf-8') + content
