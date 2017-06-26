#!/usr/bin/python
#-*-coding:utf-8-*-

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from pymongo import MongoClient


from handlers import LrcHandler
from handlers import LrcSearchHandler
from handlers import CommentHandler
from handlers import IndexHandler
from handlers import LoginHandler

from tornado.options import define, options

define("port", default=8001, type=int)
file_path = os.path.dirname(os.path.abspath(__file__))
define("log_file_prefix", default= file_path + "/tornado.log", type=str)

import ConfigParser
cfg = ConfigParser.ConfigParser()
cfg.read(file_path + "/gedeci.conf")


class Application(tornado.web.Application):
    def __init__(self, **kw):

        #mongohost = os.environ['172.17.0.2']
        mongohost = cfg.get('mongo', 'host')
        conn = MongoClient(mongohost)
        self.db = conn["lrcgc"]

        tornado.web.Application.__init__(
            self,**kw)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application(
        handlers = [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/lrcsearch", LrcSearchHandler),
            (r"/lrc", LrcHandler),
            (r"/addcomm", CommentHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "statics"),
        login_url = 'login',
        cookie_secret= "BC1C10EDF976EF60C2B4ABF949812221", # "i want to dream 2005" md5 大写
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
