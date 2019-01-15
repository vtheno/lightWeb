#coding=utf-8
class HTTPStatus(object):
    def __init__(self):
        self.http_status_map = {}
    def add(self, status: int, status_str: str) -> None:
        self.http_status_map[status] = status_str
    def __getitem__(self, status: int):
        status_str = self.http_status_map.get(status, '')
        return f"{status} {status_str}"

Status = HTTPStatus()

Status.add(100,"Continue")           # 1XX 临时性响应 client need continue request
Status.add(101,"Switching Protocols")

Status.add(200,"OK")                 # 正常处理 , GET have content , HEAD not content
Status.add(201,"Created")
Status.add(202,"Accepted")
Status.add(203,"Non-Authoritative Information")
Status.add(204,"No Content")
Status.add(205,"Reset Content")
Status.add(206,"Partial Content")    # Content-Range 指定部分的实体

Status.add(300,"Multiple Choices")
Status.add(301,"Moved Permanently")  # 永久重定向
Status.add(302,"Found")              # 临时重定向
Status.add(303,"See Other")          # like 302, use GET
Status.add(304,"Not Modified")       # 
Status.add(305,"Use Proxy")
Status.add(307,"Temporary Redirect") # like 302, 遵循标准 不变换 POST to GET

Status.add(400,"Bad Request")        # request ctx 存在语法错误
Status.add(401,"Unauthorized")       # 
Status.add(403,"Forbidden")          # 拒绝访问
Status.add(404,"Not Found")          # 
Status.add(405,"Method Not Allowed")
Status.add(406,"Not Acceptable")
Status.add(407,"Proxy Authentication Required")
Status.add(408,"Request Timeout")
Status.add(409,"Conflict")
Status.add(410,"Gone")
Status.add(411,"Length Required")
Status.add(412,"Precondition Failed")
Status.add(413,"Request Entity Too Large")
Status.add(414,"Request-URI Too Long")
Status.add(415,"Unsupported Media Type")
Status.add(416,"Requested Range Not Satisfiable")
Status.add(417,"Expectation Failed")

Status.add(500,"Internal Server Error")  # 5XX 服务器本身错误
Status.add(501,"Not Implemented")
Status.add(502,"Bad Gateway")
Status.add(503,"Service Unavailable") # 服务器繁忙
Status.add(504,"Gateway Timeout")
Status.add(505,"HTTP Version Not Supported")
__all__ = ["Status","HTTPStatus"]
