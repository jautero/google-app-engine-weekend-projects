#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Copyright 2008 Juha Autero.
#
# Copyright 2009 Juha Autero <jautero@iki.fi>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

project="Onko Mafia"
version="1.0"
author="Juha Autero <jautero@iki.fi>"
copyright="Copyright &copy; 2009 Juha Autero &lt;jautero@iki.fi&gt;."
application="onko-mafia"
import logging
import wsgiref.handlers
import os,datetime
import formats
import urlparse
from formatobjects import mafiat

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class OnkoMafia(webapp.RequestHandler):
    def get(self):
        template_values=dict(globals())
        city=self.request.get("kaupunki","helsinki").encode()
        logging.info(repr(city))
        template_values['city']=city
        template_values['netloc']=urlparse.urlparse(self.request.url).netloc
        if str(self.request.headers["User-Agent"]).find("Mac OS X") != -1:
            template_values['icalprotocol']="webcal"
        else:
            template_values['icalprotocol']="http"
        for candidate in mafiat.keys():
            if candidate==city:
                template_values[candidate+"selected"]="selected"
            else:
                template_values[candidate+"selected"]=""
        mymafiacalculator=mafiat[city]()
        format=self.request.get("format","html")        
        if format=="html":
            myformatspec=formats.get_html_format(template_values)
        elif format=="json":
            myformatspec=formats.get_json_format()
        elif format=="badge":
            myformatspec=formats.get_badge_format()
        elif format=="ical":
            self.response.headers['Content-Type']="text/calendar"
            myformatspec=formats.get_ical_format(self.request.get("upto","10"),city+" mafia")
        myformatspec.set_mafia_calculator(mymafiacalculator)
        self.response.out.write(str(myformatspec))

      
def main():
    application = webapp.WSGIApplication([('/', OnkoMafia)],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
