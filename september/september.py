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

project="September"
version="1.0"
author="Juha Autero <jautero@iki.fi>"
copyright="Copyright 2010 Juha Autero <jautero@iki.fi>"
application="september"
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from datetime import date

weekdays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
def get_timestring():
  t=date.today()
  d=(t-date(1993,8,31)).days
  if d % 10 == 1:
    ext="st"
  elif d % 10 == 2:
    ext="nd"
  elif d % 10 == 3:
    ext="rd"
  else:
    ext="th"
  return "%s September %d%s 1993" % (weekdays[t.weekday()],d,ext)

class September(webapp.RequestHandler):

  def get(self):
    template_values=globals()
    template_values["date"]=get_timestring()
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', September)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
