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

def convert_to_text(truth_value):
  if truth_value:
    return "on"
  else:
    return "ei"

class OnkoMafia(webapp.RequestHandler):

    def get(self):
        template_values=dict(globals())
        mydate=datetime.date.today()
        template_values["weekclass"]=convert_to_text(onko_mafia_week(mydate))
        template_values["weekresult"]=convert_to_text(onko_mafia_week(mydate))
        template_values["dayclass"]=convert_to_text(onko_mafia_day(mydate))
        template_values["dayresult"]=convert_to_text(onko_mafia_day(mydate))
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class FeedItem:
  def __init__(self,date,weekly):
    self.date=date
    self.day=onko_mafia_day(date)
    self.week=onko_mafia_week(date)
    self.weekly=weekly
  
  def init_feed_dict(self):
    feed_dict={}
    if self.weekly:
      feed_dict["title"]="Onko mafia tällä viikolla?"
      feed_dict["answer"]=convert_to_text(self.week)
    else:
      feed_dict["title"]="Onko mafia tänään?"
      feed_dict["answer"]=convert_to_text(self.day)
    feed_dict["date"]=self.date.ctime()
    return feed_dict
    
  def get_rss(self):
    return "<item><title>%(title)s</title><description>%(answer)s</description></item>" % self.init_feed_dict()
    
daydelta=datetime.timedelta(days=1)
weekdelta=7*daydelta

class Feed:
  def __init__(self,count=10,date=None,weekly=False):
    if not date:
      date=datetime.date.today()
    if weekly:
      date=date-date.weekday()*daydelta
    self.items=[]
    for i in range(0,count):
      self.items.append(FeedItem(date),weekly)
      if weekly:
        date=date-weekdelta
      else:
        date=date-daydelta
      
def main():
    application = webapp.WSGIApplication([('/', OnkoMafia)],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
