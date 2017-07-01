#-*-coding:utf-8-*-
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    pool = set()
    def open(self):
        EchoWebSocket.pool.add(self)

    def on_message(self, message):
        EchoWebSocket.update(self, message)
        #self.write_message(u"You said: " + message)

    def on_close(self):
        EchoWebSocket.pool.remove(self)

    @classmethod
    def update(cls, self, msg):
        for chat in cls.pool:
            if chat == self:
                continue
            chat.write_message(msg)
