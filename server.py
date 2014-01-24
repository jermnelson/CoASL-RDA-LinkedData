#-------------------------------------------------------------------------------
# Name:        server
#
# Purpose:     Flask server for CoASL Webinar Badges and Resources
#
# Author:      Jeremy Nelson
#
# Created:     2014-01-21
# Copyright:   (c) Jeremy Nelson 2014
# Licence:     GPLv2
#-------------------------------------------------------------------------------
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import datetime
import hashlib
import json
import os
import sys
import urllib2
import uuid

from flask import Flask, g, jsonify, redirect, render_template
from flask import abort, Response, url_for

app = Flask(__name__)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

IDENTITY_SALT = 'CoASL Webinar 2014'

#URL_PREFIX = "/coasl-webinar-2014"
URL_PREFIX = ""

@app.route('/coasl-webinar-participant-badge.json')
def badge_class():
    return jsonify({
        "name": "CoASL RDA and Linked Data Webinar Participation Badge",
        "description": """This Participant Badge was issued by Jeremy Nelson and intro2libsys.info for participation in the CoASL Webinar on RDA and Linked Data on 24 January 2014.""",
        "image": "http://intro2libsys.info{0}".format(
            url_for('static', filename="img/participant-badge.png")),
        "criteria": "http://intro2libsys.info/coasl-webinar-2014/",
        "tags": ["CoASL", "Special Libraries", "Linked Data", "RDA"],
        "issuer": "http://intro2libsys.info{0}".format(
            url_for('badge_issuer_org'))})

@app.route('/badge-issuer-organization.json')
def badge_issuer_org():
    return jsonify(
        {"name": "intro2libsys.info LLC",
         "url": "http://intro2libsys.info",
         "email": "jermnelson@gmail.com",
         "revocationList": "http://intro2libsys.info{0}".format(
             url_for('badge_revoked'))})

@app.route('/revoked.json')
def badge_revoked():
    return jsonify({})

@app.route("/<uid>-coasl-webinar-participant-badge.json")
def badge_for_participant(uid):
    participant_badge_location = os.path.join(PROJECT_ROOT,
                                              'badges',
                                              '{0}.json'.format(uid))
    if os.path.exists(participant_badge_location):
        participant_badge = json.load(open(participant_badge_location, 'rb'))
        if os.path.exists(os.path.join(PROJECT_ROOT,
                                       'badges',
                                       'img', '{0}.png'.format(uid))):
            participant_badge['image'] = "http://intro2libsys.info/coasl-webinar-2014/{}-coasl-webinar-participant-badge.png".format(
              uid)
        return jsonify(participant_badge)
    else:
        abort(404)

@app.route("/<uid>-coasl-webinar-participant-badge.png")
def badge_image_for_participant(uid):
    participant_img_location = os.path.join(PROJECT_ROOT,
                                            'badges',
                                            'img',
                                            '{0}.png'.format(uid))
    if os.path.exists(participant_img_location):
        img = None
        with open(participant_img_location, 'rb') as img_file:
            img = img_file.read()
        return Response(img, mimetype='image/png')
    else:
        abort(404)

def bake_badge(**kwargs):
    assert_url = kwargs.get('url')
    try:
        badge_url = 'http://beta.openbadges.org/baker?assertion={0}'.format(assert_url)
        baking_service = urllib2.urlopen(badge_url)
        raw_image = baking_service.read()
        return raw_image
    except:
        print("Exception occurred: {0}".format(sys.exc_info()))
        return None

def issue_badge(**kwargs):
    identity_hash = hashlib.sha256(kwargs.get("email"))
    identity_hash.update(IDENTITY_SALT)
    uid = str(uuid.uuid4()).split("-")[0]
    uid_url = "http://intro2libsys.info/coasl-webinar-2014/{}-coasl-webinar-participant-badge.json".format(uid)
    print(uid_url)   
    badge_json = {
        'badge': "http://intro2libsys.info/coasl-webinar-2014/coasl-webinar-participant-badge.json",
        'issuedOn': kwargs.get('issuedOne', datetime.datetime.now().isoformat()),
        'recipient': {
            'type': "email",
            'hashed': True,
            'salt': IDENTITY_SALT,
            'identity': "sha256${0}".format(
                identity_hash.hexdigest())},
        'verify': {
            'type': 'hosted',
            'url': uid_url},
        'uid': uid
        }
    # Save badge to badges directory
    json.dump(badge_json,
              open(os.path.join('badges', '{0}.json'.format(uid)), 'wb'),
              indent=2,
              sort_keys=True)
    raw_badge_img = bake_badge(url=uid_url)
    if raw_badge_img:
        with open(os.path.join('badges', 'img', '{0}.png'.format(uid)), 'wb') as img_file:
            img_file.write(raw_badge_img)
        print("Successfully added {0} and badge image".format(uid))
    else:
        print("ERROR unable to issue badge")


@app.route("/notebook")
def notebook():
    notebook = json.load(open('CoASL-RDA-Linked-data.ipynb'))
    return jsonify(notebook)

@app.route("/")
def index():
    return render_template('index.html')

def main():
    app.run(port=8002,
            host='0.0.0.0',
            debug=True)

if __name__ == '__main__':
    main()
