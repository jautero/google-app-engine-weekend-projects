#!/usr/bin/env python
# encoding: utf-8
"""
feedtask.py

Created by Juha Autero on 2010-07-07.
Copyright (c) 2010 Juha Autero. All rights reserved.
"""

import unittest
import feedparser, re
import datetime,calendar

if __name__ != '__main__':
  from google.appengine.api import urlfetch
  from google.appengine.ext import webapp
  from model import datastore
else:
  import webapptest as webapp


class feedtask(webapp.RequestHandler):
  greetingre  = re.compile("[Gg]ood [Mm]orning,?(.*)$")
  def get(self):
    data=datastore.get()
    response=urlfetch.fetch(data.url)
    if response.status_code == 200:
      if self.update_data(data,response.content):
        datastore.put()

  def update_data(self,data,content):
    feed=feedparser.parse(content)
    changed=False
    for item in feed.entries:
      result=self.greetingre.search(item.title)
      if result:
        date=datetime.datetime.fromtimestamp(calendar.timegm(item.updated_parsed))
        greeting=result.group(1)
        if date>data.latestgreeting:
          data.latestgreeting=date
          changed=True
        if not greeting in data.greetings:
          data.greetings.append(greeting)
          changed=True
    return changed

class TestData:
  pass
  
class feedtaskTests(unittest.TestCase):
  def setUp(self):
    self.data=TestData()
    self.data.greetings=[]
    self.data.latestgreeting=datetime.datetime(2010,1,1)
    
  def test_found(self):
    testobject=feedtask()
    testobject.update_data(self.data,file("test_data.rss").read())
    print self.data.greetings, self.data.latestgreeting


if __name__ == '__main__':
  unittest.main()