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
import formats,formatobjects

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class OnkoMafia(webapp.RequestHandler):

    def get(self):
        template_values=dict(globals())
        logging.info("kukkureset")
        format=self.request.get("format","html")
        if format=="html":
            myformatspec=formats.get_html_format(template_values)
        elif format=="json":
            myformatspec=formats.get_json_format()
        elif format=="badge":
            myformatspec=formats.get_badge_format()
        myformatspec.set_mafia_calculator(formatobjects.helsinki_mafia_calculator())
        logging.info("myformatspec:%s"%myformatspec)
        self.response.out.write(str(myformatspec))


      
def main():
    application = webapp.WSGIApplication([('/', OnkoMafia)],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
