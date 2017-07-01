#!/usr/bin/python
#-*-coding:utf-8-*-

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from pymongo import MongoClient
import redis


from handlers import LrcHandler
from handlers import LrcSearchHandler
from handlers import CommentHandler
#from handlers import IndexHandler
from handlers import LoginHandler
from handlers import LogoutHandler
from handlers import RegisterHandler
from handlers import EchoWebSocket

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

        redishost = cfg.get('redis', 'host')
        redisport = cfg.get('redis', 'port')
        redisdb = cfg.get('redis', 'db')
        r = redis.Redis(host=redishost,port=int(redisport),db=int(redisdb))
        self.r = r

        tornado.web.Application.__init__(
            self,**kw)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application(
        handlers = [
            #(r"/", IndexHandler),
            (r"/", LrcSearchHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/register", RegisterHandler),
            (r"/lrcsearch", LrcSearchHandler),
            (r"/lrc", LrcHandler),
            (r"/addcomm", CommentHandler),
            (r"/ws", EchoWebSocket),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "statics"),
        login_url = 'login',
        cookie_secret= "BC1C10EDF976EF60C2B4ABF949812221", # "i want to dream 2005" md5 大写
        session_secret = "BC1C10EDF976EF60C2B4ABF949812221",
        session_timeout = 10,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
