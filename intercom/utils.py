import twilio.twiml

class Intercom (object):
    """
    Take care of all the Twilio stuff.

    """
    def __init__(self, host):
        self.r = twilio.twiml.Response()
        self.host = 'http://' + host + '/'

    def greet(self):
        self.r.play(self.host + "voice/Welcome4.mp3")

    def send_to_front_desk(self):
        self.r.play(self.host + "voice/FrontDesk1.mp3")
        self.r.dial("267-702-4865")

    def notify_of_valid_code(self, member, digits):
        self.r.play(member.tone or "http://idisk.s3.amazonaws.com/tmp/9.wav")

    def notify_of_invalid_code(self, digits):
        self.r.play(self.host + "voice/Invalid3.mp3")

    def authenticate(self):
        params = dict(method='GET', action=self.host + "authenticate_member")
        with self.r.gather(**params) as auth:
            auth.play(self.host + "voice/Guest4.mp3")

    def __str__(self):
        return self.r.toxml()
