#-*-coding:utf-8-*-
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    pool = set()
    def open(self):
        EchoWebSocket.pool.add(self)
        print("WebSocket opened")

    def on_message(self, message):
        EchoWebSocket.update(u"You said: " + message)
        #self.write_message(u"You said: " + message)

    def on_close(self):
        EchoWebSocket.pool.remove(self)
        print("WebSocket closed")

    @classmethod
    def update(cls, msg):
        for chat in cls.pool:
            chat.write_message(msg)
