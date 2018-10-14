#coding=utf-8
from Web.Application import Application

import os

app = Application("static_file")
app.config["root"] = os.getcwd() + "\\"

__all__ = ["app"]
