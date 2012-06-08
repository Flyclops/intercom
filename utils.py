import couchdb
import twilio.twiml

class MemberStore (object):
    def __init__(self, config):
        db_host = config.get('MEMBER_DB_HOST')
        db_name = config.get('MEMBER_DB_NAME')
        db_args = dict(url=db_host) if db_host else {}
        self.db = couchdb.Server(**db_args)[db_name]

    def get_member_by_code(self, code):
        """
        Get an array representing the member from storage.  Return null if no
        member with the given code could be found.
        """
        try:
            member_data = self.db[code]
            return Member(self, member_data)
        except couchdb.ResourceNotFound:
            return None
        except Exception, e:
            raise Exception("Unable to get {0} : {1}".format(code, e))


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
