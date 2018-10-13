#coding=utf-8
class HttpStatus(object):
    def __init__(self,code : int ,desc : str):
        self.code = str(code)
        self.desc  = desc
    def __str__(self):
        return f"{self.code} {self.desc}"
    def __repr__(self):
        return str(self)
    def __iter__(self):
        return iter([self.code,self.desc])

Continue    = HttpStatus(100,"Continue")           # 1XX 临时性响应 client need continue request
Switch      = HttpStatus(101,"Switching Protocols")

OK          = HttpStatus(200,"OK")                 # 正常处理 , GET have content , HEAD not content
Created     = HttpStatus(201,"Created")
Accepted    = HttpStatus(202,"Accepted")
NonAuth     = HttpStatus(203,"Non-Authoritative Information")
NoContent   = HttpStatus(204,"No Content")
ResetContent= HttpStatus(205,"Reset Content")
PartContent = HttpStatus(206,"Partial Content")    # Content-Range 指定部分的实体

MultChoices = HttpStatus(300,"Multiple Choices")
MovePerm    = HttpStatus(301,"Moved Permanently")  # 永久重定向
Found       = HttpStatus(302,"Found")              # 临时重定向
SeeOther    = HttpStatus(303,"See Other")          # like 302, use GET
NotModified = HttpStatus(304,"Not Modified")       # 
UseProxy    = HttpStatus(305,"Use Proxy")
TempRedire  = HttpStatus(307,"Temporary Redirect") # like 302, 遵循标准 不变换 POST to GET

BadRequest  = HttpStatus(400,"Bad Request")        # request ctx 存在语法错误
UnAuth      = HttpStatus(401,"Unauthorized")       # 
Forbidden   = HttpStatus(403,"Forbidden")          # 拒绝访问
NotFound    = HttpStatus(404,"Not Found")          # 
NotAllow    = HttpStatus(405,"Method Not Allowed")
NotAccept   = HttpStatus(406,"Not Acceptable")
ProxyAuth   = HttpStatus(407,"Proxy Authentication Required")
Timeout     = HttpStatus(408,"Request Timeout")
Conflict    = HttpStatus(409,"Conflict")
Gone        = HttpStatus(410,"Gone")
RequireLen  = HttpStatus(411,"Length Required")
PreFailed   = HttpStatus(412,"Precondition Failed")
TooLarge    = HttpStatus(413,"Request Entity Too Large")
TooLong     = HttpStatus(414,"Request-URI Too Long")
UnSupport   = HttpStatus(415,"Unsupported Media Type")
NoRange     = HttpStatus(416,"Requested Range Not Satisfiable")
ExceptFail  = HttpStatus(417,"Expectation Failed")

InternalSE  = HttpStatus(500,"Internal Server Error")  # 5XX 服务器本身错误
NoImplement = HttpStatus(501,"Not Implemented")
BadGateway  = HttpStatus(502,"Bad Gateway")
Unavailable = HttpStatus(503,"Service Unavailable") # 服务器繁忙
GatewayOut  = HttpStatus(504,"Gateway Timeout")
NotSupport  = HttpStatus(505,"HTTP Version Not Supported")
