#coding=utf-8
from Web.Application import Application

import os

app = Application("static_file")
app.config["root"] = os.getcwd() + "\\"
app.config["www"] = app.config["root"] + "www\\"
app.config["static"] = app.config["www"] + "static\\"
__all__ = ["app"]
