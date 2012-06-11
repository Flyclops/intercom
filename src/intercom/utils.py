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
        # self.r.play(self.host + "voice/FrontDesk1.mp3")
        self.r.dial("267-702-4865")

    def notify_of_valid_code(self, member, digits):
        self.r.play(member.tone or "http://idisk.s3.amazonaws.com/tmp/9.wav")

    def notify_of_invalid_code(self, digits):
        self.r.play(self.host + "voice/Invalid3.mp3")

    def authenticate(self):
        # Copy the verbs off of the response so far, and put them inside of the
        # gather.  We don't want the user to have to wait until the gather
        # starts to be able to give their input; it should all be in the gather.

        verbs = self.r.verbs[:]
        self.r.verbs = []
        params = dict(method='GET', action=self.host + "authenticate_member")
        with self.r.gather(**params) as auth:
            auth.verbs = verbs[:]
            auth.play(self.host + "voice/Guest6.mp3")

    def __str__(self):
        return self.r.toxml()
