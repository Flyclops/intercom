"""
Flask Documentation:     http://flask.pocoo.org/docs/

This file creates your application.
"""

import os
import sys

# Make sure this file's path is in the PYTHONPATH (for utils and settings).
sys.path.append(os.path.dirname(__file__))

import utils
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Try to load settings from the 'settings.py' file.  If the module does not
# exist, try loading from environment variables.
#
# Environment:
# -----------
# * SECRET_KEY
#   An arbitrary string
#
# * MEMBER_DB_HOST (optional)
#   In the form 'http://[user:pass@]www.mycouchserver.com:1234/'.  Note that
#   you must use user:pass if your database is not in admin-party (it shouldn't
#   be).
#
# * MEMBER_DB_NAME
#   The name of the specific member database

try:
    import settings
    app.config.from_object(settings)
except ImportError:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['MEMBER_DB_HOST'] = os.environ.get('MEMBER_DB_HOST')
    app.config['MEMBER_DB_NAME'] = os.environ['MEMBER_DB_NAME']


###
# Routing for your application.
###

@app.route('/first_contact')
def first_contact():
    r = utils.Responder(request.url_root)
    r.redirect_to_authentication("voice/Welcome4.mp3")

    return (str(r), 200, {'Content-type': 'text/xml'})


@app.route('/authenticate_member')
def authenticate_member():
    digits = request.values['Digits']
    r = utils.Responder(request.url_root)

    if digits == '0':
        r.redirect_to_front_desk()

    else:
        db = utils.MemberStore(app.config)
        member = db.get_member_by_code(digits)
        r.authenticate_member(member)

    return (str(r), 200, {'Content-type': 'text/xml'})


@app.route('/voice/<file_name>.mp3')
def send_voice_file(file_name):
    return app.send_static_file('voice/' + file_name + '.mp3')


if __name__ == '__main__':
    app.run(debug=True)
