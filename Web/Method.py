#coding=utf-8
class Method(type):
    def __new__(cls,name,parents,attrs):
        return name
class GET(metaclass=Method):     pass # 1.1 1.0
class POST(metaclass=Method):    pass # 1.1 1.0
class PUT(metaclass=Method):     pass # 1.1 1.0
class HEAD(metaclass=Method):    pass # 1.1 1.0
class DELETE(metaclass=Method):  pass # 1.1 1.0
class OPTIONS(metaclass=Method): pass # 1.1 
class TRACE(metaclass=Method):   pass # 1.1 
class CONNECT(metaclass=Method): pass # 1.1 
methods = [GET,POST,PUT,HEAD,DELETE,OPTIONS,TRACE,CONNECT]
