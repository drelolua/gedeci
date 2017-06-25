#-*-coding:utf-8-*-
from urllib2 import urlopen
from urllib import quote
from bs4 import BeautifulSoup
from pymongo import MongoClient
from redis import Redis

client = MongoClient()
db = client.lrcgc
col = db.lrcs

r = Redis()

host = "http://www.lrcgc.com/"
artlisturl = "artist-00.html"

def getSonglist(url):
    res = urlopen(url)
    #print("Request status code %d" % res.code)
    html = res.read()
    bso = BeautifulSoup(html, "html.parser")
    name = bso.find("div",{"class":"bread_crumb"}).find_all("a")[-1].string
    alist = bso.find("tbody").find_all("a",{"class":"ico-lrc"})
    if len(alist) < 1:
        return False
    alist.append(name)
    return alist

def getLrc(href):
    try:
        url = host + quote(href.encode("gbk"))
    except Exception:
        return False
    res = urlopen(url)
    content = res.read()
    return content

def getArt(artid):
    n = 1
    url = host + "songlist-%d-%d.html"%(artid, n)
    alist = getSonglist(url)
    if alist == False:
        retrycount = int(r.get("lcrretry"))
        if retrycount < 100:
            r.incr("lcrretry", 1)
            return True
        else:
            r.set("lcrretry", 0)
            return False
    while True:
        n = r.get("lcrpage")
        n = int(n)
        url = host + "songlist-%d-%d.html"%(artid, n)
        alist = getSonglist(url)
        if alist:
            name = alist[-1]
            for a in alist[:-1]:
                href = a.attrs["href"]
                songname = "".join(href.split("/")[1:]).replace(".lrc", "")
                content = getLrc(href)
                if content:
                    col.insert_one({"artist":name, "lrc":content, "songname":songname})
            r.incr("lcrpage")
            n = int(r.get("lcrpage"))
        else:
            break
    r.set("lcrpage", 1)

    return True

r.set("lcrretry", 0)
while True:
    aid = r.get("lcrartistid")
    try:
        res = getArt(int(aid))
    except Exception as e:
        r.set("lcrretry", 0)
        r.incr("lcrartistid")
        continue
    if res:
        r.incr("lcrartistid")
    else:
        print("Break")
        break
