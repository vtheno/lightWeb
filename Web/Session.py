#coding=utf-8
from time import time, sleep
from random import choice
import threading

def random(size:int) -> str:
    s = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    return ''.join([choice(s) for i in range(size)])

class Session(dict):
    def __init__(self,id:str,live_time:float):
        self.live_time = live_time
        self.id = id
        dict.__init__(self)
    def set_time(self):
        self.recent_time = time()
    def can_gc(self):
        return time() >= self.recent_time + self.live_time
class Sessions(object):
    def __init__(self, live_time: float=50):
        self.sessions = {}
        self.live_time = live_time
        threading._start_new_thread(self.gc_session,())
    def build_session(self) -> Session:
        id = random(32)
        while id in self.sessions.keys():
            id = random(32)
        self.sessions[id] = Session(id,self.live_time)
        self.sessions[id].set_time()
        return self.sessions[id]
    def get_session(self,key :str):
        return self.sessions.get(key,None)
    def update_session(self, ctx: "Request") -> Session:
        """
        if session not live then dorp it and create new session and update cookie
        else session is live then update recent_time
        """
        key = ctx.request.get_session()
        print( f"1 => {ctx.request.url}" )
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
        ctx.response.push( f"Set-Cookie: session={session.id}; httpOnly; path=/" ) 
        return session

    def unset_session(self, key : str) -> None:
        if key in self.sessions.keys():
            self.sessions.pop(key)
                
    def gc_session(self):
        while 1:
            for k,v in self.sessions.items():
                if v.can_gc():
                    print( f"gc => {v.id}" )
                    self.sessions.pop( k )
                    break
            sleep(0.05)

__all__ = ["Session", "Sessions"]
