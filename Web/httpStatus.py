#coding=utf-8
class HTTPStatus(object):
    def __init__(self,code : int ,desc : str):
        self.code = str(code)
        self.desc  = desc
    def __str__(self):
        return f"{self.code} {self.desc}"
    def __repr__(self):
        return str(self)
    def __iter__(self):
        return iter([self.code,self.desc])

Continue    = HTTPStatus(100,"Continue")           # 1XX 临时性响应 client need continue request
Switch      = HTTPStatus(101,"Switching Protocols")

OK          = HTTPStatus(200,"OK")                 # 正常处理 , GET have content , HEAD not content
Created     = HTTPStatus(201,"Created")
Accepted    = HTTPStatus(202,"Accepted")
NonAuth     = HTTPStatus(203,"Non-Authoritative Information")
NoContent   = HTTPStatus(204,"No Content")
ResetContent= HTTPStatus(205,"Reset Content")
PartContent = HTTPStatus(206,"Partial Content")    # Content-Range 指定部分的实体

MultChoices = HTTPStatus(300,"Multiple Choices")
MovePerm    = HTTPStatus(301,"Moved Permanently")  # 永久重定向
Found       = HTTPStatus(302,"Found")              # 临时重定向
SeeOther    = HTTPStatus(303,"See Other")          # like 302, use GET
NotModified = HTTPStatus(304,"Not Modified")       # 
UseProxy    = HTTPStatus(305,"Use Proxy")
TempRedire  = HTTPStatus(307,"Temporary Redirect") # like 302, 遵循标准 不变换 POST to GET

BadRequest  = HTTPStatus(400,"Bad Request")        # request ctx 存在语法错误
UnAuth      = HTTPStatus(401,"Unauthorized")       # 
Forbidden   = HTTPStatus(403,"Forbidden")          # 拒绝访问
NotFound    = HTTPStatus(404,"Not Found")          # 
NotAllow    = HTTPStatus(405,"Method Not Allowed")
NotAccept   = HTTPStatus(406,"Not Acceptable")
ProxyAuth   = HTTPStatus(407,"Proxy Authentication Required")
Timeout     = HTTPStatus(408,"Request Timeout")
Conflict    = HTTPStatus(409,"Conflict")
Gone        = HTTPStatus(410,"Gone")
RequireLen  = HTTPStatus(411,"Length Required")
PreFailed   = HTTPStatus(412,"Precondition Failed")
TooLarge    = HTTPStatus(413,"Request Entity Too Large")
TooLong     = HTTPStatus(414,"Request-URI Too Long")
UnSupport   = HTTPStatus(415,"Unsupported Media Type")
NoRange     = HTTPStatus(416,"Requested Range Not Satisfiable")
ExceptFail  = HTTPStatus(417,"Expectation Failed")

InternalSE  = HTTPStatus(500,"Internal Server Error")  # 5XX 服务器本身错误
NoImplement = HTTPStatus(501,"Not Implemented")
BadGateway  = HTTPStatus(502,"Bad Gateway")
Unavailable = HTTPStatus(503,"Service Unavailable") # 服务器繁忙
GatewayOut  = HTTPStatus(504,"Gateway Timeout")
NotSupport  = HTTPStatus(505,"HTTP Version Not Supported")
