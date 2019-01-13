#coding=utf-8
from Web.Route import *
from Web.Request import Request

import time
import re

def build_route_regexp(string):
    def named_groups(obj):
        # old '(?P<{obj}>[a-zA-Z0-9_]+)'
        return '(?P<{obj}>(.+))'.format(obj=obj.group(1))
    re_string = re.sub(
        r'{([a-zA-Z0-9_]+)}', 
        named_groups,
        string.replace('?','\?').replace('*','\*').replace('+','\+')
    )
    re_string = '^' + re_string + '$'
    print( re_string )
    return re.compile(re_string) 

class Application(object):
    def __init__(self,name : str):
        self.__name__ = name             # __name__ : str
        self._route = Route({})          # _route : Route
        self.lookup = self._route.lookup # lookup : Request -> Response
        self.config = {}                 # config : {str:str}
        
    def __repr__(self):
        return f"{self._route!r}"

    def route(self,pattern : str):
        pattern = build_route_regexp(pattern)
        def wait(fn):
            self._route.route_table.update( {pattern:fn} )
            return fn
        return wait

    def add_route(self, pattern : str , fn ):
        pattern = build_route_regexp(pattern)
        self._route.route_table.update( {pattern:fn} )
        return None

__all__ = ["Application"]
