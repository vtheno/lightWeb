#coding=utf-8
from time import time

class Session(dict):
    def __init__(self,id:str,live_time:float):
        self.live_time = live_time
        self.id = id
        dict.__init__(self)
    def set_time(self):
        self.recent_time = time()
    def can_gc(self):
        return time() - self.recent_time >= self.live_time

__all__ = ["Session"]
