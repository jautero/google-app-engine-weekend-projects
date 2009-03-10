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
    if onko_mafia_week(date) and date.weekday()==3:
        return True
    else:
        return False

def convert_to_text(truth_value,valuestrings=("on","ei")):
  if truth_value:
    return valuestrings[0]
  else:
    return valuestrings[1]

class OnkoMafia(webapp.RequestHandler):

    def get(self):
        template_values=dict(globals())
        mydate=datetime.date.today()
        format=self.request.get("format","html")
        if format=="banner":
            img_index=0
            if onko_mafia_day(mydate):
                img_index+=1
            if onko_mafia_week(mydate):
                img_index+=2
            path=os.path.join(os.path.dirname(__file__),"banner_%d.png" % img_index)
        if format=="html":
            self.set_html_template_values(template_values,onko_mafia_week(mydate),onko_mafia_day(mydate))
            path=os.path.join(os.path.dirname(__file__),'index.html')
        elif format=="json":
            self.set_json_template_values(template_values,onko_mafia_week(mydate),onko_mafia_day(mydate))
            path=os.path.join(os.path.dirname(__file__),'index.json')
        elif format=="badge":
            self.set_badge_template_values(template_values,onko_mafia_week(mydate),onko_mafia_day(mydate))
            path=os.path.join(os.path.dirname(__file__),'badge.js')
            
        self.response.out.write(template.render(path, template_values))

    def set_html_template_values(self,template_values,mafia_week,mafia_day):
        template_values["weekclass"]=convert_to_text(mafia_week)
        template_values["weekresult"]=convert_to_text(mafia_week)
        template_values["dayclass"]=convert_to_text(mafia_day)
        template_values["dayresult"]=convert_to_text(mafia_day)

    def set_json_template_values(self,template_values,mafia_week,mafia_day):
<<<<<<< HEAD:onko-mafia/onko-mafia.py
        if mafia_week:
            template_values["weekresult"]="true"
        else:
            template_values["weekresult"]="false"
        if mafia_day:
            template_values["dayresult"]="true"
        else:
            template_values["dayresult"]="false"
=======
        template_values["weekresult"]=convert_to_text(mafia_week,("true","false"))
        template_values["dayresult"]=convert_to_text(mafia_day,("true","false"))
>>>>>>> c696bf3443fe7aa6c9f45f97f761d2e411375830:onko-mafia/onko-mafia.py

<<<<<<< HEAD:onko-mafia/onko-mafia.py
    def set_badge_template_values(self,template_values,mafia_week,mafia_day):
        if mafia_week:
            template_values["weekcolor"]="#00ff00"
            template_values["weekword"]="on"
        else:
            template_values["weekcolor"]="#ff0000"
            template_values["weekword"]="ei"
            
        if mafia_day:
            template_values["daycolor"]="#00ff00"
            template_values["dayword"]="on"
        else:
            template_values["daycolor"]="#ff0000"
            template_values["dayword"]="ei"
            
=======
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
      
>>>>>>> c696bf3443fe7aa6c9f45f97f761d2e411375830:onko-mafia/onko-mafia.py
def main():
    application = webapp.WSGIApplication([('/', OnkoMafia)],
                                        debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
