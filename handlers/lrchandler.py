#-*- coding:utf-8 -*-

import tornado.web
import tornado.escape
from bson import ObjectId

from basehandlers import BaseHandler


#class LrcSearchHandler(tornado.web.RequestHandler):
class LrcSearchHandler(BaseHandler):
    def get(self):
        songname = self.get_argument('s', False)
        if songname == False:
            self.render("lrc/searchlist.html",lrcs=[],title=u"搜索歌词")
            return
        db = self.application.db
        col = db.lrcs
        lrcs_cur = col.find({"songname":{"$regex":songname}},{"songname":1, "_id":1}).limit(20)
        if lrcs_cur==None:
            self.write(u"<h1>没有收录 <strong>%s</strong> 的歌词. ✧(≖ ◡ ≖✿)嘿嘿</h1>"%songname)
            return
        lrcs = list(lrcs_cur)
        for lrc in lrcs:
            lrc["_id"] = str(lrc['_id'])

        self.render("lrc/searchlist.html",lrcs=lrcs,title=u"搜索歌词")

#class LrcHandler(tornado.web.RequestHandler):
class LrcHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        lrcid = self.get_argument("lrcid", False)
        if lrcid == False:
            self.render("lrc/lrc.html", lrcs = [], title=u"没有歌词啊")
            return
        db = self.application.db
        lrc = db.lrcs.find_one({"_id":ObjectId(lrcid)})
        lrcstr = lrc["lrc"].replace(u"歌词千寻", u"歌的词")
        lrcstr = lrcstr.replace("www.lrcgc.com", 'www.gedeci.com')
        commentls = lrc.get("commentlist", [])
        user = self.my_session['user']
        self.render("lrc/lrc.html",
                    lrcid=lrcid,
                    title=lrc["songname"],
                    lrcs=lrcstr.split("\n"),
                    commentls=commentls,
                    user = user,
                    next_url = tornado.escape.url_escape("/lrc?lrcid="+lrcid)
                    )

class CommentHandler(tornado.web.RequestHandler):
    '''
    def get(self):
        pass
        #self.write(self.get_argument("user", "unknow user"))
    '''
    def post(self):
        db = self.application.db
        lrcid = self.get_argument("lrcid", False)
        obid = ObjectId(lrcid)
        comment_id = str(ObjectId())
        user = self.get_argument("user", "unknow user")
        comm = self.get_argument("comm", "no comment")
        db.lrcs.update_one(
                {"_id":obid},
                {"$push":{
                    "commentlist":{
                        "user":user,
                        "comm":comm,
                        "id":comment_id
                    }
                }}
            )
        '''
        doc = {
            "user":user,
            "comm":comm,
            "lrcid":lrcid
        }
        '''
        #self.write(doc)
        self.redirect('/lrc?lrcid='+lrcid)


class AddLrcHandler(BaseHandler):
    def get(self):
        self.render('/addlrc.html')

    def post(self):
        db = self.application.db
        lrc_content = self.get_argument('content')
        title = self.get_argument('title')
        tags = self.get_argument('tags')
        copyright = self.get_argument('copyright')
        lrc = dict(
            title = title,
            content = lrc_content,
            tags = tags,
            copyright = copyright
        )
        res = db.lrcs.insert_one(lrc)
        self.redirect('/lrc?lrcid='+res.id)
