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
OK = HttpStatus(200,"OK")
NotFound = HttpStatus(404,"Not Found")
# HTTP/1.1
# how implement format function 
