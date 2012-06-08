import twilio.twiml

class MemberStore (object):
    def __init__(self, config):
        import pymongo
        from urlparse import urlparse

        db_url = config.get('MEMBER_DB_URL')
        parts = urlparse(db_url)

        db_host = parts.hostname
        db_port = parts.port
        db_name = parts.path[1:]
        db_user = parts.username
        db_pass = parts.password

        self.db = pymongo.Connection(db_host, db_port)[db_name]
        self.db.authenticate(db_user, db_pass)
        self.collection = self.db['members']

    def get_member_by_code(self, code):
        """
        Get an array representing the member from storage.  Return null if no
        member with the given code could be found.
        """
        data = self.collection.find_one({'code': code})
        if data:
            return Member(self, data)
        else:
            return None


class Member (object):
    def __init__(self, store, data):
        self.store = store
        self.data = data

    @property
    def tone(self):
        """
        Get the tone from the given member array, or fall back to some default.
        """
        if 'tone' in self.data:
            return self.data['tone']
        return "http://idisk.s3.amazonaws.com/tmp/9.wav";


class Responder (object):
    """
    Take care of all the Twilio stuff.

    """
    def __init__(self, host):
        self.r = twilio.twiml.Response()
        self.host = host

    def redirect_to_front_desk(self):
        self.r.play(self.host + "voice/FrontDesk1.mp3")
        self.r.dial("267-702-4865")

    def authenticate_member(self, member):
        if member is not None:
            self.r.play(member.tone)
        else:
            self.redirect_to_authentication("voice/Invalid3.mp3")

    def redirect_to_authentication(self, message):
        params = dict(
            action=self.host + "authenticate_member",
            method='GET'
        )
        with self.r.gather(**params) as auth:
            auth.play(self.host + message)
            auth.play(self.host + "voice/Guest4.mp3")

    def __str__(self):
        return self.r.toxml()
