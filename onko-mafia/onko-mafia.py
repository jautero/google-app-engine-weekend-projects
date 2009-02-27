#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Copyright 2008 Juha Autero
#
# Copyright 2009 Juha Autero <jautero@iki.fi>
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
copyright="Copyright &copy; 2009 Juha Autero <jautero@iki.fi>"
application="onko-mafia"
import logging
import wsgiref.handlers
import os,datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

month_lengths=[31,28,31,30,31,30,31,31,30,31,30,31]
def is_leapyear(year):
  return (X%4==0 and X%100!=0 or x%400==0)

def year_day(date):
  if is_leapyear(date.year) and date.month > 2:
    # Add leap day
    return sum(month_lengths[0:date.month-1])+date.day+1
  else:
    return sum(month_lengths[0:date.month-1])+date.day
  
def weekno(date):
    year_weekday=datetime.date(date.year,1,1).weekday()
    weekno=((year_day(date)-1)+year_weekday)/ 7
    if year_weekday in range(0,4):
        weekno+=1
    if (weekno==53):
        if not year_weekday==3 or (year_weekday==2 and is_leapyear(date.year)):
            weekno=1
    if (weekno==0):
        year_weekday=datetime.date(date.year-1,1,1).weekday()
        if year_weekday==3 or (year_weekday==2 and is_leapyear(date.year-1)):
            weekno=53
        else:
            weekno=52
    return weekno
        
def onko_mafia_week(date):
    return weekno(date) % 2 == 1
                
def onko_mafia_day(date):
    logging.info("Time: %s",date.ctime())
    if onko_mafia_week(date) and date.tm_wday==3:
        return True
    else:
        return False

class OnkoMafia(webapp.RequestHandler):

    def get(self):
        template_values=dict(globals())
        mydate=datetime.date.today()
        if onko_mafia_week(mydate):
            template_values["weekclass"]="on"
            template_values["weekresult"]="on"
        else:
            template_values["weekclass"]="ei"
            template_values["weekresult"]="ei"
        if onko_mafia_day(mydate):
            template_values["dayclass"]="on"
            template_values["dayresult"]="on"
        else:        
            template_values["dayclass"]="ei"
            template_values["dayresult"]="ei"
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([('/', OnkoMafia)],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
