#coding=utf-8
from Web.Route import *
from Web.Check import AssertCheck

class Application(object):
    def __init__(self,name : str):
        self.__name__ = name            # __name__ : str
        self._route = Route({})         # _route : Route
        self.lookup = self._route.route # lookup : Request -> Response
        self.config = {}                # config : {str:str}
    def __repr__(self):
        return f"{self._route!r}"
    def route(self,pattern_str : str):
        AssertCheck(pattern_str , str)
        #print( f"{self.__name__}: define route {pattern_str}" )
        pattern = Pattern(pattern_str)
        def wait(fn):
            self._route.route_table[pattern] = fn
            return lambda *args,**kw: self._route.route(*args,**kw)
        return wait
__all__ = ["Application"]
