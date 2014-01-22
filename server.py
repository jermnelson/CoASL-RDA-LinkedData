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
from flask import Flask

app = Flask(__name__)

PREFIX = "/coasl-rda-ld-2014"

@app.route("/")
#@app.route("{0}/".format(PREFIX))
def index():
    return "In CoASL Webinar Badge and Resources"

def main():
    app.run(port=8002,
            host='0.0.0.0',
            debug=True)

if __name__ == '__main__':
    main()
