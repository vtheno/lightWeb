#coding=utf-8
from Web.Application import Application
import os

app = Application(__name__)
app.config["root"] = os.getcwd()
app.config["www"] = app.config["root"] + "\\www\\"
app.config["static"] = app.config["www"] + "\\static\\"
app.config["vue"] = app.config["www"] + "\\vue\\"

__all__ = ["app"]
