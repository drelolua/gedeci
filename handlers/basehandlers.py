#-*-coding:utf-8-*-
import tornado.web
from tornado.log import logging

from session import SessionRedis as Session


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.my_session = Session(self)

    def get_current_user(self):
        #return self.get_cookie(Session.session_id)
        return self.get_secure_cookie("user")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        #greeting = self.get_argument('greeting', 'Hello')
        #self.write(greeting + ", friendly user!")
        self.redirect("/lrcsearch")

class LoginHandler(BaseHandler):
    def get(self):
        '''
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
        '''
        self.render("login.html", action="register")

    def post(self):
        username = self.get_argument("name")
        password = self.get_argument("password")
        #email = self.get_argument("email")
        logging.info({"username":username,"password":password})
        db = self.application.db
        user = db.users.find_one({"name":username})
        if user == None:
            self.redirect("login")
        if username == user['name'] and password == user['password']:
            self.my_session['user'] = username
            self.my_session['pwd'] = password
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect('/login')
        #self.set_secure_cookie("__sessionId__", create_session_id())

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html",action="register")

    def post(self):
        username = self.get_argument("name")
        password = self.get_argument("password")
        email = self.get_argument("email")
        db = self.application.db
        user_col = db.users
        result = user_col.insert_one({"name":username, "password":password, "email":email})
        if result.acknowledged:
            self.redirect("/login")
        else:
            self.redirect("/register")
