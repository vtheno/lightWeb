
cdef class HTTPRequest:
    cpdef str msg
    cpdef str forms
    cpdef str method_route_version
    cpdef list infos
    cpdef public str method
    cpdef public str url
    cpdef public str http_version
    cpdef public dict info
    cpdef public dict form
    def __init__(self, str inp):
        self.msg, self.forms = inp.split("\r\n\r\n")
        self.method_route_version, *self.infos = [i for i in self.msg.split("\r\n") if i]
        self.method, self.url, self.http_version = self.method_route_version.split()
        self.method = self.method.upper()
    cpdef void parseInfo(self):
        self.info = dict([(k.lower(),v) for k,v in [tuple(o.split(': ')) for o in self.infos]])
    cpdef void parseForm(self):
        self.form = dict([tuple(i.split("=")) for i in self.forms.split("&") if i])
    cpdef object get_session(self):
        cookie = self.info.get("cookie")
        if cookie:
            key,value = tuple(cookie.split("="))
            if key == "session" and value:
                return value
        return None
cdef class HTTPResponse:
    cpdef public str headers
    cpdef public str status
    cpdef public str content
    cpdef public bytes b_content
    cpdef str buff
    def __init__(self):
        self.headers = ''
        self.status = "200 OK"
        self.content = ""
        self.b_content = bytes()
        self.buff = "\r\n"
    cpdef void push(self, str header):
        self.headers += header + '\r\n'
    cpdef bytes build_with_string(self):
        self.buff += self.headers + '\r\n'
        self.buff += self.content
        self.buff = '\r\n'.join([
            f"HTTP/1.1 {self.status}",
            "Server: lightWeb"
        ]) + self.buff
        return bytes(self.buff, 'utf-8')
    cpdef bytes build_with_bytes(self):
        self.buff += self.headers + '\r\n'
        self.buff = '\r\n'.join([
            f"HTTP/1.1 {self.status}",
            "Server: lightWeb"
        ]) + self.buff
        return bytes(self.buff, 'utf-8') + self.b_content
