#-*-coding:utf-8-*-
from hashlib import sha1
import os,time
import cPickle as pickle

session_container = {}
create_session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()


class Session(object):
    session_id = '__sessionId__'

class SessionMemory(Session):

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

class SessionRedis(Session):

    def __init__(self, request):
        session_value = request.get_cookie(Session.session_id)
        self.r = request.application.r
        if not session_value:
            self._id = create_session_id()
        else:
            self._id = session_value
        request.set_cookie(Session.session_id,  self._id)

    def __getitem__(self, key):
       mashed_session =  self.r.get(self._id)
       session = pickle.loads(mashed_session)
       return session

    def __setitem__(self, key, value):
        mashed_session =  self.r.get(self._id)
        if mashed_session:
            session = pickle.loads(mashed_session)
            session[key] = value
            remashed_session = pickle.dumps(session)
            self.r.set(self._id, remashed_session)
        else:
            session = {key:value}
            remashed_session = pickle.dumps(session)
            self.r.set(self._id, remashed_session)

    def __delitem__(self, key):
        mashed_session = self.r.ge(self._id)
        session = pickle.loads(mashed_session)
        del session[key]
        remashed_session = pickle.dumps(session)
        self.r.set(self._id, remashed_session)

