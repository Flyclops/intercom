import twilio.twiml

class Intercom (object):
    """
    Take care of all the Twilio stuff.

    """
    def __init__(self, host):
        self.r = twilio.twiml.Response()
        self.host = 'http://' + host + '/'

    def greet(self):
        params = dict(method='GET', action=self.host + "authenticate", numDigits=1, timeout=0)
        with self.r.gather(**params) as hello:
            hello.say("Welcome to Flyclops. One moment please.", language="en-gb", voice="female")
        self.send_to_front_desk()

    def send_to_front_desk(self):
        self.r.dial("267-603-2206", hangupOnStar=True, callerId="267-234-7335")
        #self.r.dial("856-236-7846", hangupOnStar=True, callerId="267-234-7335")

    def notify_of_valid_code(self, member, digits):
        self.r.play("http://com-flyclops-hyperstatic.s3.amazonaws.com/com-flyclops-intercom/91.wav", loop=5)

    def notify_of_invalid_code(self, digits):
        self.send_to_front_desk()

    def authenticate(self):
        # Copy the verbs off of the response so far, and put them inside of the
        # gather.  We don't want the user to have to wait until the gather
        # starts to be able to give their input; it should all be in the gather.
        verbs = self.r.verbs[:]
        self.r.verbs = []
        params = dict(method='GET', action=self.host + "authenticate_member", numDigits=6, timeout=10)
        with self.r.gather(**params) as auth:
            auth.verbs = verbs[:]
            auth.say("Greetings Flyclopsian.", language="en-gb", voice="female")
        self.send_to_front_desk()

    def __str__(self):
        return self.r.toxml()
