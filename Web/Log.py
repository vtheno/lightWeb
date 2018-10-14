#coding=utf-8
import logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Log(object):
    def __init__(self,filename="Server.log"):
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.logfile = logging.FileHandler(filename,mode="w")
        self.logfile.setLevel(logging.INFO)
        self.logfile.setFormatter(
            logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            )
        self.log.addHandler(self.logfile)
        self.debug = self.log.debug
        self.info  = self.log.info
        self.warning = self.log.warning
        self.error   = self.log.error
        self.critical = self.log.critical

Log = Log()
__all__ = ["Log"]
