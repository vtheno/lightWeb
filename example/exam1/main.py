#coding=utf-8
from Web.Server import HTTPServer

from app import app
from static import app

if __name__ == '__main__':
    HTTPServer(app,'0.0.0.0', 80).start()
