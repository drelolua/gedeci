#-*-coding:utf-8-*-
import tornado.web
from tornado.log import logging
from hashlib import sha1
import os,time

session_container = {}
create_session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()

class Session(object):
    session_id = '__sessionId__'

    def __init__(self, request):
        session_value = request.get_cookie(Session.session_id)
        if not session_value:
            self._id = create_session_id()
        else:
            self._id = session_value

        #request.set_secure_cookie
        request.set_cookie(Session.session_id, self._id)

    def __getitem__(self, key):
        return session_container[self._id][key]

    def __setitem__(self, key, value):
        if session_container.has_key(self._id):
            session_container[self._id][key] = value
        else:
            session_container[self._id] = {key:value}

    def __delitem__(self, key):
        del session_container[self._id][key]


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
