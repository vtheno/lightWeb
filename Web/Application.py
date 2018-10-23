#coding=utf-8
from Web.Route import *
from Web.Session import *
from Web.Request import Request
from Web.Header import Set_Cookie
from Web.Tool import call
import time
from random import choice

def random(size:int) -> str:
    s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    return ''.join([choice(s) for i in range(size)])

class Application(object):
    def __init__(self,name : str):
        self.__name__ = name            # __name__ : str
        self._route = Route({})         # _route : Route
        self.lookup = self._route.route # lookup : Request -> Response
        self.config = {}                # config : {str:str}
        self.sessions = {}

    def build_session(self,live_time:float=50) -> Session:
        id = random(32)
        while id in self.sessions.keys():
            id = random(32)
        self.sessions[id] = Session(id,live_time)
        self.sessions[id].set_time()
        return self.sessions[id]

    def get_session(self,key :str):
        if key in self.sessions.keys():
            return self.sessions[key]
        return None
    def update_session(self,ctx:Request) -> Session:
        """
        if session not live then dorp it and create new session and update cookie
        else session is live then update recent_time
        """
        key = ctx.get_session_key()
        print( f"1 => {ctx.get_url()}" )
        print( f"2 => sessions {self.sessions}" )
        if key:
            session = self.get_session(key)
            print( f"3 => session {session}")
            if session:
                print( f"4 => {session.id} not,update" )
                session.set_time()
                return session
        session = self.build_session()
        session["login"] = False
        print( f"4 => {session.id} update" )
        ctx.add_general(Set_Cookie(f"session={session.id}; httpOnly; path=/"))
        return session

    def unset_session(self,key : str) -> None:
        if key in self.sessions.keys():
            @self.sessions.pop
            @call
            def _():
                return key

    def gc_session(self):
        while 1:
            for k,v in self.sessions.items():
                if v.can_gc():
                    print( f"gc => {v.id}" )
                    @self.sessions.pop
                    @call
                    def _():
                        return k
                    break
            time.sleep(0.05)

    def __repr__(self):
        return f"{self._route!r}"

    def route(self,pattern_str : str):
        #print( f"{self.__name__}: define route {pattern_str}" )
        pattern = Pattern(pattern_str)
        def wait(fn):
            @self._route.route_table.update
            @call
            def _():
                return {pattern:fn}
            return self._route.route
        return wait

    def add_route(self, pattern_str : str , fn ):
        pattern = Pattern(pattern_str)
        @self._route.route_table.update
        @call
        def _():
            return {pattern:fn}
        return None

__all__ = ["Application"]
