#!/usr/bin/env python
# encoding: utf-8
"""
feedtask.py

Created by Juha Autero on 2010-07-07.
Copyright (c) 2010 Juha Autero. All rights reserved.
"""

import unittest
import feedparser, re

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from model import datastore


class feedtask(webapp.RequestHandler):
  greetingre  = re.compile("[Gg]ood [Mm]orning,? \(.*\)$")
  def get(self):
    data=datastore.get()
    response=urlfetch.fetch(data.url)
    if response.status_code == 200:
      feed=feedparser.parse(response.content)
      changed=False
      for item in feed.entries:
        result=self.greetingre.search(item.title)
        if result:
          date=item.pubDate
          greeting=result.group(1)
          if date>data.latestgreeting:
            data.latestgreeting=date
            changed=True
          if not greeting in data.greetings:
            data.greetings.append(greeting)
            changed=True
      if changed:
        data.put()

class feedtaskTests(unittest.TestCase):
  def setUp(self):
    pass


if __name__ == '__main__':
  unittest.main()