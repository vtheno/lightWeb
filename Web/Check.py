#coding=utf-8
def AssertCheck(obj,typ):
    if not isinstance(obj,typ):
        raise TypeError(f"isinstance({obj},{typ})")
__all__ = ["AssertCheck"]
