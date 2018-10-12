#coding=utf-8
# general header => self.general
class Header(type):
    def __new__(cls,name,parents,attrs):
        attrs["__name__"] = name.replace("_","-")
        attrs["__call__"] = lambda self,inp:f"{self.__name__}: {inp}"
        return type.__new__(cls,name,parents,attrs)()

class Cache_Control(metaclass=Header): pass

class Connection(metaclass=Header): pass

class Date(metaclass=Header): pass

class Pragma(metaclass=Header): pass

class Trailer(metaclass=Header): pass

class Transfer(metaclass=Header): pass

class Upgrade(metaclass=Header): pass

class Via(metaclass=Header): pass

class Warn(metaclass=Header): pass

# response header => self.header
class Location(metaclass=Header): pass

# content header => self.header
class Content_length(metaclass=Header): pass

class Content_type(metaclass=Header): pass

class Content_encoding(metaclass=Header): pass

class Content_lang(metaclass=Header): pass

class Allow(metaclass=Header): pass

class Set_Cookie(metaclass=Header): pass
