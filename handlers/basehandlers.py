#-*-coding:utf-8-*-
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
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
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html",action="register")

    def post(self):
        pass
