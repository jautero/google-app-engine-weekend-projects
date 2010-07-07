#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Copyright 2008 Juha Autero
#
# Copyright 2010 Juha Autero <jautero@iki.fi>
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

project="Good Morning Feeder"
version="1.0"
author="Juha Autero <jautero@iki.fi>"
copyright="Copyright 2010 Juha Autero <jautero@iki.fi>"
application="good-morning-feeder"
import wsgiref.handlers
import os, random, datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from model import datastore

class GoodMorningFeeder(webapp.RequestHandler):

  timeofdaynames=["morning","afternoon","evening","night"]

  def get(self):
    template_values=globals()
    data = datastore.get()
    template_values["greeting"]="Good %s %s" % (self.get_timeofday(data.latestgreeting),random.choice(datastore.greetings))
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

  def get_timeofday(self,timestamp):
    return self.timeofdaynames[(datetime.datetime.now()-timestamp).seconds/(3600*6)]

def main():
  application = webapp.WSGIApplication([('/', GoodMorningFeeder)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
